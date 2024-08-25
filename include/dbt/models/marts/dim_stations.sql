WITh dim_stations AS (
    SELECT
        station_id,
        station_name,
        phone_number,
        address,
        status,
        created_datetime,
        update_datetime
    FROM {{ ref('stations') }}
)
SELECT 
    {{ dbt_utils.generate_surrogate_key(['station_id']) }} as station_sk,
    *
FROM dim_stations