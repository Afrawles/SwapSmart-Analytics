FROM quay.io/astronomer/astro-runtime:12.0.0


# # Install gcc and other necessary build tools
# RUN apt-get update && apt-get install -y \
#     gcc \
#     build-essential \
#     python3-dev \
#     libpq-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-core && \
    pip install --no-cache-dir dbt-postgres && \
    pip install --no-cache-dir dbt-bigquery && deactivate 

RUN python -m venv soda_venv && source soda_venv/bin/activate && \
    pip install --no-cache-dir soda-core-bigquery && \
    pip install --no-cache-dir soda-core-postgres && deactivate
    # pip install --no-cache-dir soda-core-scientific && deactivate
