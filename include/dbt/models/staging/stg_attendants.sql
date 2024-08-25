WITH raw_attendants AS (
    SELECT
        attendant_id,
        first_name,
        last_name,
        email,
        phone_number,
        address,
        status,
        created_datetime,
        update_datetime
    FROM {{ source("postgres","attendants") }}
)
SELECT *
FROM raw_attendants