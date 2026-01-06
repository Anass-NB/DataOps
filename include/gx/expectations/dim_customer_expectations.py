import great_expectations as gx
from great_expectations.expectations import (
    ExpectColumnToExist,
    ExpectColumnValuesToBeOfType,
    ExpectColumnValuesToBeUnique,
    ExpectColumnValuesToNotBeNull,
)

# Create expectation suite
suite_name = "dim_customer_suite"

# Define expectations as a list
expectations = []

# Schema: Required columns (matching dbt model: dim_customer.sql)
required_columns = ["customer_key", "country"]
for col in required_columns:
    expectations.append(
        ExpectColumnToExist(column=col)
    )

# Schema: Column types
column_types = {
    "customer_key": "str",
    "country": "str",
}
for col, dtype in column_types.items():
    expectations.append(
        ExpectColumnValuesToBeOfType(column=col, type_=dtype)
    )

# All customers are unique
expectations.append(
    ExpectColumnValuesToBeUnique(column="customer_key")
)

# All customers have a key (no nulls)
expectations.append(
    ExpectColumnValuesToNotBeNull(column="customer_key")
)