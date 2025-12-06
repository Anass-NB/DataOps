{{ config(materialized='table') }}

select
    invoiceno as invoice_number,
    stockcode as product_key,
    customerid as customer_key,
    invoicedate as datetime_key,
    quantity,
    unitprice,
    quantity * unitprice as total
from {{ source('retail', 'orders_raw') }}