SELECT
  dc.address,
  dc.last_name,
  COUNT(ft.transaction_id) AS total_transactions,
  SUM(ft.transaction_amount) AS total_revenue
FROM {{ ref('fct_transaction_history') }} ft
JOIN {{ ref('dim_clients') }} dc ON ft.client_sk = dc.client_sk
GROUP BY dc.address, dc.last_name
ORDER BY total_revenue DESC
LIMIT 10