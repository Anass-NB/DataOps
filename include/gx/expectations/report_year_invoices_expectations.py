import great_expectations as gx
from great_expectations.expectations import (
    ExpectColumnValuesToBeBetween,
)

# Create expectation suite
suite_name = "report_year_invoices_suite"

# Define expectations as a list
expectations = []

# Number of invoices is non-negative
expectations.append(
    ExpectColumnValuesToBeBetween(column="num_invoices", min_value=0)
)