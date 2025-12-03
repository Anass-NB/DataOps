{{ config(materialized='view') }}

SELECT
    COUNTRY,
    COUNT(*) AS number_of_orders
FROM RAW.ORDERS_RAW
GROUP BY COUNTRY