SELECT
  da.address,
  da.last_name,
  COUNT(ft.transaction_id) AS total_transactions,
  SUM(ft.transaction_amount) AS total_revenue
FROM {{ ref('fct_transaction_history') }} ft
JOIN {{ ref('dim_attendants') }} da ON ft.attendant_sk = da.attendant_sk
GROUP BY da.address, da.last_name
ORDER BY total_revenue DESC
LIMIT 10