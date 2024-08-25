WITH raw_bikes AS (
    SELECT
        bike_id,
        client_id,
        status,
        created_datetime,
        update_datetime
    FROM {{ source("postgres","bikes") }}
)
SELECT *
FROM raw_bikes