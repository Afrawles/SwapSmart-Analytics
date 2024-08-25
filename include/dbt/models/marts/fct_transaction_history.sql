WITH fct_transaction_history AS (
    SELECT
        client_id,
        transaction_id,
        battery_given_out,
        battery_received,
        bike_id,
        station_id,
        attendant_id,
        battery_given_soc,
        battery_received_soc,
        battery_usage_diff,
        discount,
        transaction_amount,
        TO_DATE(SUBSTRING(timestamp FROM 1 FOR 8), 'DD-MM-YY') AS transaction_date
        FROM {{ ref('stg_transactions') }}

)
SELECT
    COALESCE(dclients.client_sk, '-1') AS client_sk,
    COALESCE(dstations.station_sk, '-1') AS station_sk,
    COALESCE(dattendants.attendant_sk, '-1') AS attendant_sk,
    COALESCE(dbikes.bike_sk, '-1') AS bike_sk,
    fct.transaction_id,
    fct.transaction_date,
    fct.battery_given_out,
    fct.battery_received,
    fct.bike_id,
    fct.station_id,
    fct.attendant_id,
    fct.battery_given_soc,
    fct.battery_received_soc,
    fct.battery_usage_diff,
    COALESCE(fct.discount, 'No Discount') AS discount,
    fct.transaction_amount
FROM fct_transaction_history as fct
LEFT JOIN {{ ref('dim_stations') }} AS dstations
    ON fct.station_id = dstations.station_id
LEFT JOIN {{ ref('dim_clients') }} AS dclients
    ON fct.client_id = dclients.client_id
LEFT JOIN {{ ref('dim_attendants') }} AS dattendants
    ON fct.attendant_id = dattendants.attendant_id
LEFT JOIN {{ ref('dim_bikes') }} AS dbikes
    ON fct.bike_id = dbikes.bike_id