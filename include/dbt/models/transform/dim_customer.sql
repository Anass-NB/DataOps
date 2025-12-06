{{ config(materialized='table') }}

select distinct
    customerid as customer_key,
    customerid as customer_id,
    country
from {{ source('retail', 'orders_raw') }}
where customerid is not null