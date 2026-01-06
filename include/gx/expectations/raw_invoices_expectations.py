import great_expectations as gx
from great_expectations.expectations import (
    ExpectColumnToExist,
    ExpectColumnValuesToBeOfType,
)

# Create expectation suite
suite_name = "raw_invoices_suite"

# Define expectations as a list
expectations = []

# Schema: Required columns exist
required_columns = ["InvoiceNo", "StockCode", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID", "Country"]
for col in required_columns:
    expectations.append(
        ExpectColumnToExist(column=col)
    )

# Schema: Column types
column_types = {
    "InvoiceNo": "str",
    "StockCode": "str",
    "Quantity": "int64",
    "InvoiceDate": "str",
    "UnitPrice": "float64",
    "CustomerID": "float64",
    "Country": "str",
}
for col, dtype in column_types.items():
    expectations.append(
        ExpectColumnValuesToBeOfType(column=col, type_=dtype)
    )