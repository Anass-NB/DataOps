SELECT DISTINCT
    INVOICENO as product_id,
	StockCode AS stock_code,
    Description AS description,
    UnitPrice AS price
FROM {{ source('raw_data', 'orders_raw') }}
WHERE UnitPrice < 0
