{{ config(materialized='table') }}

with cleaned as (

    select distinct
        -- convert varchar to timestamp
        to_timestamp(invoiceDate, 'MM/DD/YYYY HH24:MI') as datetime_key,
        to_timestamp(invoiceDate, 'MM/DD/YYYY HH24:MI') as invoicedate
    from {{ source('retail', 'orders_raw') }}

)

select
    datetime_key,
    invoicedate,
    year(invoicedate) as year,
    month(invoicedate) as month,
    day(invoicedate) as day
from cleaned