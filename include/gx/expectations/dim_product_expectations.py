import great_expectations as gx
from great_expectations.expectations import (
    ExpectColumnToExist,
    ExpectColumnValuesToBeOfType,
    ExpectColumnValuesToBeUnique,
    ExpectColumnValuesToNotBeNull,
    ExpectColumnValuesToBeInSet,
)

# Create expectation suite
suite_name = "dim_product_suite"

# Define expectations as a list
expectations = []

# Schema: Required columns (matching dbt model: dim_product.sql)
required_columns = ["product_key", "product_name", "product_category"]
for col in required_columns:
    expectations.append(
        ExpectColumnToExist(column=col)
    )

# Schema: Column types
column_types = {
    "product_key": "str",
    "product_name": "str",
    "product_category": "str",
}
for col, dtype in column_types.items():
    expectations.append(
        ExpectColumnValuesToBeOfType(column=col, type_=dtype)
    )

# All products are unique
expectations.append(
    ExpectColumnValuesToBeUnique(column="product_key")
)

# All products have a key (no nulls)
expectations.append(
    ExpectColumnValuesToNotBeNull(column="product_key")
)

# Product category should be one of the expected values
expectations.append(
    ExpectColumnValuesToBeInSet(column="product_category", value_set=["Decor", "Homeware", "Other"])
)