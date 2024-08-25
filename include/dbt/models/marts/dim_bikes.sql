WITH dim_bikes AS (
    SELECT
        bike_id,
        client_id,
        status,
        created_datetime,
        update_datetime
    FROM {{ ref('bikes') }}
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['sdb.bike_id', 'sdb.client_id']) }} AS bike_sk,
    sdb.bike_id,
    sdb.client_id,
    sdb.status,
    sdb.created_datetime,
    sdb.update_datetime,
    dclients.first_name,
    dclients.last_name
FROM dim_bikes sdb
LEFT JOIN {{ ref('dim_clients') }} AS dclients
ON sdb.client_id = dclients.client_id

