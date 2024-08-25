WITH raw_transactions AS (
    SELECT
        transaction_id,
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
    FROM {{ source("postgres","transactions") }}
)
SELECT *
FROM raw_transactions