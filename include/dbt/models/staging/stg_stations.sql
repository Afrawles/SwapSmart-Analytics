WITH raw_stations AS (
    SELECT
        station_id,
        station_name,
        phone_number,
        address,
        status,
        created_datetime,
        update_datetime
    FROM  {{ source("postgres","stations") }}
)
SELECT *
FROM raw_stations