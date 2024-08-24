import os
import ast
import csv
import random

from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.constants import LoadMode
from cosmos.config import RenderConfig


from dataclasses import asdict

from faker import Faker
from google.cloud import storage

from utils.helpers import (
    generate_transactions,
    generate_bikes,
    generate_clients,
    generate_battery,
    generate_attendants,
    generate_station,
    data_insert_queries,
    DataParser
    )

from utils.db import DBConnection
from include.dbt.cosmos_config import DBT_CONFIG, DBT_PROJECT_CONFIG

def load_generated_data(nclients: int = 1000):
    fake = Faker()
    # dsn = os.environ.get('DB_DSN')
    dsn = Variable.get("secret_dsn", default_var=None)

    status_1 = {'active', 'inactive'}
    status_2 = {'active', 'inactive', 'maintenance'}
    
    station_names = {
        "Najjera", "Gulu Town", "Mbarara", "Fort Portal", "Kireka", "Jinja",
        "Mbuya I", "Muyenga", "Ntinda", "Nakaseero", "Entebbe", "Bwaise",
        "Mpigi", "Masaka", "Masindi", "Moroto Town", "Kumi Town", "Soroti", "Sseta"
    }

    clients = [asdict(generate_clients(i, status_1, fake)) for i in range(1, nclients+1)]
    batteries = [asdict(generate_battery(i, status_2, fake)) for i in range(1, nclients*3)]
    bikes = [asdict(generate_bikes(i, random.choice(clients)['client_id'], status_2, fake)) for i in range(1, nclients-50)]
    stations = [asdict(generate_station(i, status_1, fake, n)) for i, n in enumerate(station_names, start=1)]
    attendants = [asdict(generate_attendants(i, status_1, fake)) for i in range(len(station_names)*2)]
    
    transactions = [
        asdict(generate_transactions(
            random.choice(clients)['client_id'],
            random.choices(batteries, k=2),
            random.choice(bikes)['bike_id'],
            random.choice(stations)['station_id'],
            random.choice(attendants)['attendant_id'],
            fake
        )) for n in range(1000)
    ]
    
    data = {
        "clients": clients,
        "batteries": batteries,
        "bikes": bikes,
        "stations": stations,
        "attendants": attendants,
        "transactions": transactions
    }

    saver = PostgresDataSaver(data, dsn=dsn)
    saver.save()


class PostgresDataSaver(DataParser):
    def __init__(self, data: dict, dsn: str, insert_queries = data_insert_queries()):
        super().__init__(data)
        self.dsn = dsn
        self.insert_queries = insert_queries

    def save(self):
        with DBConnection(self.dsn).manage_conn() as cursor:
            try:
                for table_name, values in self.data.items():
                    values = [tuple(x.values()) for x in values]
                    if table_name == 'transactions':
                        cursor.execute("BEGIN") 
                        for transaction in values:
                            cursor.execute(
                                self.insert_queries['transactions'],
                                transaction
                            )
                        cursor.execute("COMMIT")
                    else:
                        cursor.executemany(self.insert_queries[table_name], values)
            except Exception as e:
                cursor.execute("ROLLBACK") 
                print(f"Error occurred: {e}")



class GCSDataSaver(DataParser):
    def __init__(self, data, conn_id='google_cloud_default', bucket_name='swapsmart', output_dir='raw/'):
        super().__init__(data)
        self.conn_id = conn_id
        self.bucket_name = bucket_name
        self.output_dir = output_dir

    def save(self):
        data = ast.literal_eval(data)
        client = storage.Client.from_service_account_json('/usr/local/airflow/include/gcp/service_account.json')
        bucket = client.bucket('swapsmart') 
        
        for key, records in data.items():
            output_file = os.path.join(self.output_dir, f'{key}_{datetime.now().strftime("%Y%m%d")}.csv')
            blob = bucket.blob(output_file)
            
            with blob.open("wt") as file:
                writer = csv.DictWriter(file, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)
@dag(
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['data_generation'],
    template_searchpath='/usr/local/airflow/setup_postgres',
    )
def generate_data():
    
    create_tables_task = PostgresOperator(
        task_id="setup_schema",
        postgres_conn_id="swapsmart",
        sql="setup.sql",
    )

    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load_generated_data,
    )

    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_load(scan_name='check_load', checks_subpath='sources'):
        from include.soda.check_function import check
        
        return check(scan_name, checks_subpath)

    staging_data = DbtTaskGroup(
        group_id="staging_data",
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=["path:models/staging"]
        ),
    )

    transform_data = DbtTaskGroup(
        group_id="transform_data",
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=["path:models/marts"]
        ),
    )

    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_transform(scan_name='check_transform', checks_subpath='marts'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)

    report = DbtTaskGroup(
        group_id='report',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/report']
        )
    )

    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_report(scan_name='check_report', checks_subpath='report'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)
    
    create_tables_task >> load_task >> check_load() >> staging_data >> transform_data >> check_transform() >> report >> check_report()

generate_data()