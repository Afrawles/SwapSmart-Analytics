SELECT
  dt.month_name,
  dt.day_of_week_name,
  COUNT(DISTINCT ft.transaction_id) AS num_transactions,
  SUM(ft.transaction_amount) AS total_revenue
FROM {{ ref('fct_transaction_history') }} ft
JOIN {{ ref('dim_date') }} dt ON ft.transaction_date = dt.date_day
GROUP BY dt.month_name, dt.day_of_week_name
ORDER BY dt.month_name, dt.day_of_week_name