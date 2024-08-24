WITH raw_batteries AS (
    SELECT
        battery_id,
        capacity,
        status,
        created_datetime,
        update_datetime
    FROM {{ source("postgres","batteries") }}
)
SELECT *
FROM raw_batteries