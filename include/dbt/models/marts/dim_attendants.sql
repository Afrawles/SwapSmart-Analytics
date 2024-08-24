WITh stg_dim_attendants AS (
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
    FROM {{ ref("stg_attendants") }}
)
SELECT 
    {{ dbt_utils.generate_surrogate_key(["attendant_id"]) }} as attendant_sk,
    *
FROM stg_dim_attendants