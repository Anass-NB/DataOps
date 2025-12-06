{{ config(materialized='table') }}

select distinct
    stockcode as product_key,
    stockcode as stock_code,
    description
from {{ source('retail', 'orders_raw') }}