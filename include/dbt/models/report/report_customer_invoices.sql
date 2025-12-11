SELECT
  c.country,
  COUNT(fi.invoice_number) AS total_invoices,
  SUM(fi.total) AS total_revenue
FROM {{ ref('fct_invoices') }} fi
JOIN {{ ref('dim_customer') }} c ON fi.customer_key= c.customer_id
GROUP BY c.country
ORDER BY total_revenue DESC
LIMIT 10