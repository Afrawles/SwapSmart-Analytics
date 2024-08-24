WITH raw_clients AS (
    SELECT
        client_id,
        first_name,
        last_name,
        email,
        phone_number,
        address,
        status,
        created_datetime,
        update_datetime
    FROM {{ source("postgres","clients") }}
)
SELECT *
FROM raw_clients