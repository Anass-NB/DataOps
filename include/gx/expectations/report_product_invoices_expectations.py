import great_expectations as gx
from great_expectations.expectations import (
    ExpectColumnValuesToNotBeNull,
    ExpectColumnValuesToBeBetween,
)

# Create expectation suite
suite_name = "report_product_invoices_suite"

# Define expectations as a list
expectations = []

# All products have a stock code (no nulls)
expectations.append(
    ExpectColumnValuesToNotBeNull(column="stock_code")
)

# Total quantity sold is greater than 0
expectations.append(
    ExpectColumnValuesToBeBetween(column="total_quantity_sold", min_value=1)
)