WITH dim_batteries as (
    SELECT
        battery_id,
        capacity,
        status,
        created_datetime,
        update_datetime
    FROM {{ ref('stg_batteries') }}
) 
SELECT 
    {{ dbt_utils.generate_surrogate_key(['battery_id']) }} as battery_sk,
    * 
FROM dim_batteries