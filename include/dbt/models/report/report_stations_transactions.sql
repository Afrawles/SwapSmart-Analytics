SELECT
  ds.address,
  ds.station_name,
  COUNT(ft.transaction_id) AS total_transactions,
  SUM(ft.transaction_amount) AS total_revenue
FROM {{ ref('fct_transaction_history') }} ft
JOIN {{ ref('dim_stations') }} ds ON ft.station_sk = ds.station_sk
GROUP BY ds.address, ds.station_name
ORDER BY total_revenue DESC
LIMIT 10