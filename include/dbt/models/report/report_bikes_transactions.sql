SELECT
  db.bike_id,
  db.client_id,
  db.last_name,
  SUM(ft.transaction_amount) AS total_transaction_amount_swapped
FROM {{ ref('fct_transaction_history') }} ft
JOIN {{ ref('dim_bikes') }} db ON ft.bike_sk = db.bike_sk
GROUP BY db.bike_id, db.client_id, db.last_name
ORDER BY total_transaction_amount_swapped DESC
LIMIT 10