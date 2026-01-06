import great_expectations as gx
from great_expectations.expectations import (
    ExpectColumnValuesToNotBeNull,
    ExpectColumnValuesToBeBetween,
)

# Create expectation suite
suite_name = "report_customer_invoices_suite"

# Define expectations as a list
expectations = []

# All customers have a country (no nulls)
expectations.append(
    ExpectColumnValuesToNotBeNull(column="country")
)

# Total invoices is greater than 0
expectations.append(
    ExpectColumnValuesToBeBetween(column="total_invoices", min_value=1)
)