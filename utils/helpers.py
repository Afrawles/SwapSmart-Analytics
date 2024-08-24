import time
import ast
import random
from typing import List, Set, Dict
from abc import ABC, abstractmethod

from .models import (
    Discount,
    Client,
    Battery,
    Bike,
    Station,
    Transaction,
    Attendants
)


class DataParser(ABC):
    def __init__(self, data):
        self.data = data
        # self.data = self._parse_data(data)
    
    def _parse_data(self, data):
        """
        Parse the input Xcom data from a string to a dict.
        """
        return ast.literal_eval(data)
    
    @abstractmethod
    def save(self):
        pass


# helper function for calculating transation amount
def calc_amount_paid(usage: int, discount: Discount, max_price: int = 10_000) -> float:
    match discount:
        case Discount.NO.value:
            return float(usage / 100 * max_price)
        case Discount.FIFTY.value:
            return float(usage / 100 * max_price) * .5
        case Discount.SEVENTYFIVE.value:
            return float(usage / 100 * max_price) * .25
        case Discount.HUNDRED.value:
            return 0.0
        case default:
            raise ValueError(f"Unknown discount: {discount}")

def generate_clients(client_id: int, status: set, fake) -> Client:
    """
    Generate Fake Client data
    Args:
    """
    
    fake_date = fake.date_this_decade().isoformat()
    return Client(client_id,
                  fake.first_name(),
                  fake.last_name(),
                  fake.email(),
                  fake.phone_number(),
                  fake.address(),
                  random.choice(tuple(status)),
                  fake_date,
                  fake_date)

def generate_bikes(bike_id: int, client_id: int, status: set, fake) -> Bike:
    """
    bike_id: int
    client_id: int
    status: str # active  | inactive | maintenance
    purchase_datetime: str
    update_datetime: str
    """
    fake_date = fake.date_this_decade().isoformat()
    return Bike(
        bike_id,
        client_id,
        random.choice(tuple(status)),
        fake_date,
        fake_date
    )

def generate_battery(battery_id: int, status: set, fake, capacity: List[int] = [37, 40]) -> Battery:
    """
    battery_id: int
    capacity: int
    status: str # active | inactive | maintenance 
    manufacture_datetime: str
    update_datetime: str
    """
    fake_date = fake.date_this_decade().isoformat()
    return Battery(
        battery_id,
        random.choice(capacity),
        random.choice(tuple(status)),
        fake_date,
        fake_date
    )


def generate_station(station_id: int, status: set, fake, station_name: str) -> Station:
    """
    station_id: int
    station_name: str
    phone_number: str
    address: str
    status: str # active  | inactive
    created_datetime: str
    update_datetime: str
    """

    fake_date = fake.date_this_decade().isoformat()
    return Station(
        station_id,
        station_name,
        fake.phone_number(),
        fake.address(),
        random.choice(tuple(status)),
        fake_date,
        fake_date
    )

def generate_attendants(attendant_id: int, status: Set[Battery], fake) -> Attendants:
    """
    attendant_id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    address: str
    employment_status: str # active  | inactive
    created_datetime: str
    update_datetime: str   
    """
    fake_date = fake.date_this_decade().isoformat()
    return Attendants(
        attendant_id,
        fake.first_name(),
        fake.last_name(),
        fake.email(),
        fake.phone_number(),
        fake.address(),
        random.choice(tuple(status)),
        fake_date,
        fake_date
    )


def generate_transactions(
        # transaction_id: int, 
        client_id: int,
        battery_ids: List,
        bike_id: int,
        station_id: int,
        attendant_id: int,
        fake
        ) -> Transaction:
    """
    transaction_id: int
    created_datetime: str
    client_id: int
    battery_given_id: int
    battery_received_id: int
    bike_id: int
    station_id: int
    attendant_id: int
    battery_given_percentage: int
    battery_recevived_percentage: int
    battery_usage_diff: int
    discount: str
    transaction_amount: float
    """
    # A few assumptions are made e.g
    # we always giving out % >= 90
    # we alwys getting  batteries w/ % <= 50
    soc_batt_given: int = random.randint(90, 100)
    soc_batt_received: int = random.randint(0, 50)
    usage_diff: int = soc_batt_given - soc_batt_received

    discount = fake.random_element(elements=(
                Discount.NO.value, 
                Discount.FIFTY.value, 
                Discount.SEVENTYFIVE.value, 
                Discount.HUNDRED.value
                ))
    transaction_amount: float = calc_amount_paid(usage_diff, discount)

    # Generate a random time interval in seconds (between 5 and 3600 seconds)
    time_interval = random.randint(1, 3600)

    timestamp = time.strftime("%y-%m-%d %H:%M:%S", time.localtime(time.time() + time_interval))

    return Transaction(
        # transaction_id,
        timestamp,
        client_id,
        battery_ids[0]['battery_id'],
        battery_ids[1]['battery_id'],
        bike_id,
        station_id,
        attendant_id,
        soc_batt_given,
        soc_batt_received,
        usage_diff,
        discount,
        transaction_amount
    )

# helper function for queries used to insert
# data in postgres
def data_insert_queries() -> Dict[str, str]:
    clients: str = """
    INSERT INTO swapsmart_schema.clients (
        client_id,
        first_name,
        last_name,
        email,
        phone_number,
        address,
        status,
        created_datetime,
        update_datetime
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (client_id) 
    DO UPDATE SET
        (
            first_name, 
            last_name, 
            email, 
            phone_number, 
            address, 
            status, 
            update_datetime
        ) = (
        EXCLUDED.first_name, 
        EXCLUDED.last_name,
        EXCLUDED.email,
        EXCLUDED.phone_number,
        EXCLUDED.address,
        EXCLUDED.status,
        EXCLUDED.update_datetime
        );
"""
    batteries: str = """
    INSERT INTO swapsmart_schema.batteries (
        battery_id,
        capacity,
        status,
        created_datetime,
        update_datetime
    ) VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (battery_id) 
    DO UPDATE SET
        (
            capacity, 
            status,
            update_datetime
        ) = (
        EXCLUDED.capacity, 
        EXCLUDED.status,
        EXCLUDED.update_datetime
        );
"""
    attendants: str = """
    INSERT INTO swapsmart_schema.attendants (
        attendant_id,
        first_name,
        last_name,
        email,
        phone_number,
        address,
        status,
        created_datetime,
        update_datetime
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (attendant_id) 
    DO UPDATE SET
        (
            first_name, 
            last_name, 
            email, 
            phone_number, 
            address, 
            status, 
            update_datetime
        ) = (
        EXCLUDED.first_name, 
        EXCLUDED.last_name,
        EXCLUDED.email,
        EXCLUDED.phone_number,
        EXCLUDED.address,
        EXCLUDED.status,
        EXCLUDED.update_datetime
        );
"""

    bikes: str = """
    INSERT INTO swapsmart_schema.bikes (
        bike_id,
        client_id,
        status,
        created_datetime,
        update_datetime
    ) VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (bike_id) 
    DO UPDATE SET
        (
            client_id, 
            status,
            update_datetime
        ) = (
        EXCLUDED.client_id, 
        EXCLUDED.status,
        EXCLUDED.update_datetime
        );
"""
    stations: str = """
    INSERT INTO swapsmart_schema.stations (
        station_id,
        station_name,
        phone_number,
        address,
        status,
        created_datetime,
        update_datetime
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (station_id) 
    DO UPDATE SET
        (
            station_name,
            phone_number, 
            address, 
            status, 
            update_datetime
        ) = (
        EXCLUDED.station_name,
        EXCLUDED.phone_number,
        EXCLUDED.address,
        EXCLUDED.status,
        EXCLUDED.update_datetime
        );
"""

    transactions: str = """
    INSERT INTO swapsmart_schema.transactions (
        timestamp,
        client_id,
        battery_given_out,
        battery_received,
        bike_id,
        station_id,
        attendant_id,
        battery_given_soc,
        battery_received_soc,
        battery_usage_diff,
        discount,
        transaction_amount
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (client_id, timestamp) 
    DO NOTHING;
"""
    return {
        'clients': clients,
        'bikes': bikes,
        'stations': stations,
        'attendants': attendants,
        'batteries': batteries,
        'transactions': transactions
    } 
