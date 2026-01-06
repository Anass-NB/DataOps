import great_expectations as gx
from great_expectations.expectations import (
    ExpectColumnToExist,
    ExpectColumnValuesToNotBeNull,
    ExpectColumnValuesToBeUnique,
    ExpectColumnValuesToBeBetween,
)

# Create expectation suite
suite_name = "fct_invoices_suite"

# Define expectations as a list
expectations = []

# Schema: Required columns (matching dbt model: fact_sales.sql)
required_columns = ["line_id", "invoiceno", "product_key", "customer_key", "date_key", "quantity", "unit_price", "line_amount"]
for col in required_columns:
    expectations.append(
        ExpectColumnToExist(column=col)
    )

# All line_ids have a key (no nulls)
expectations.append(
    ExpectColumnValuesToNotBeNull(column="line_id")
)

# All line_ids are unique
expectations.append(
    ExpectColumnValuesToBeUnique(column="line_id")
)

# Unit price should be non-negative
expectations.append(
    ExpectColumnValuesToBeBetween(column="unit_price", min_value=0)
)