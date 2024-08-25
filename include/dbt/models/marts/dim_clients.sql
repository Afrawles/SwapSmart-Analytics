WITh dim_clients AS (
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
    FROM {{ ref("clients") }}
)
SELECT 
    {{ dbt_utils.generate_surrogate_key(['client_id']) }} as client_sk,
    *
FROM dim_clients