SELECT
  dt.year,
  dt.month,
  COUNT(DISTINCT fi.invoice_number) AS num_invoices,
  SUM(fi.total) AS total_revenue
FROM {{ ref('fct_invoices') }} fi
JOIN {{ ref('dim_datetime') }} dt ON fi.datetime_key = dt.datetime_key
GROUP BY dt.year, dt.month
ORDER BY dt.year, dt.month