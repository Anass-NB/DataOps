import great_expectations as gx
from great_expectations.expectations import (
    ExpectColumnToExist,
    ExpectColumnValuesToBeUnique,
    ExpectColumnValuesToNotBeNull,
    ExpectColumnValuesToBeBetween,
)

# Create expectation suite
suite_name = "dim_datetime_suite"

# Define expectations as a list
expectations = []

# Schema: Required columns (matching dbt model: dim_date.sql)
required_columns = ["date_key", "full_date", "year", "month", "day"]
for col in required_columns:
    expectations.append(
        ExpectColumnToExist(column=col)
    )

# All date keys are unique
expectations.append(
    ExpectColumnValuesToBeUnique(column="date_key")
)

# All date keys have a value (no nulls)
expectations.append(
    ExpectColumnValuesToNotBeNull(column="date_key")
)

# Month values should be between 1 and 12
expectations.append(
    ExpectColumnValuesToBeBetween(column="month", min_value=1, max_value=12)
)

# Day values should be between 1 and 31
expectations.append(
    ExpectColumnValuesToBeBetween(column="day", min_value=1, max_value=31)
)