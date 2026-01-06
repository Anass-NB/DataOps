"""
Great Expectations Snowflake Validator Module

This module provides functionality to validate data in Snowflake tables
using Great Expectations suites defined in the expectations folder.
"""

import os
import logging
from typing import Dict, Any, Optional, List
import great_expectations as gx

logger = logging.getLogger(__name__)

# Mapping of table names to their expectation suite modules
TABLE_SUITE_MAPPING = {
    # Raw layer
    "ORDERS_RAW": "raw_invoices_expectations",
    
    # Core dimension tables (dbt models)
    "dim_customer": "dim_customer_expectations",
    "dim_date": "dim_datetime_expectations",
    "dim_product": "dim_product_expectations",
    
    # Fact tables (dbt models)
    "fact_sales": "fct_invoices_expectations",
}


def get_snowflake_connection_string() -> str:
    """Build Snowflake connection string from environment variables."""
    from urllib.parse import quote_plus
    
    account = os.environ.get("SNOWFLAKE_ACCOUNT")
    user = os.environ.get("SNOWFLAKE_USER")
    password = os.environ.get("SNOWFLAKE_PASSWORD")
    database = os.environ.get("SNOWFLAKE_DATABASE", "ECOMMERCE_DB")
    warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE", "ecommerce_warehouse")
    schema = os.environ.get("SNOWFLAKE_SCHEMA", "ANALYTICS")
    role = os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN")
    
    # URL-encode password to handle special characters like @
    encoded_password = quote_plus(password) if password else ""
    
    return f"snowflake://{user}:{encoded_password}@{account}/{database}/{schema}?warehouse={warehouse}&role={role}"


def load_expectation_suite(suite_module_name: str):
    """
    Dynamically load expectations from the expectations folder.
    
    Args:
        suite_module_name: Name of the module (without .py extension)
        
    Returns:
        Tuple of (suite_name, expectations list)
    """
    import importlib.util
    import sys
    
    expectations_path = os.path.join(
        os.path.dirname(__file__), 
        "expectations", 
        f"{suite_module_name}.py"
    )
    
    spec = importlib.util.spec_from_file_location(suite_module_name, expectations_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[suite_module_name] = module
    spec.loader.exec_module(module)
    
    return module.suite_name, module.expectations


def validate_table(
    table_name: str,
    schema: str = "ANALYTICS",
    database: str = "ECOMMERCE_DB",
    raise_on_failure: bool = True
) -> Dict[str, Any]:
    """
    Validate a Snowflake table using its mapped expectation suite.
    
    Args:
        table_name: Name of the table to validate
        schema: Snowflake schema name
        database: Snowflake database name
        raise_on_failure: Whether to raise an exception on validation failure
        
    Returns:
        Dictionary containing validation results
    """
    if table_name not in TABLE_SUITE_MAPPING:
        raise ValueError(f"No expectation suite found for table: {table_name}")
    
    suite_module = TABLE_SUITE_MAPPING[table_name]
    suite_name, expectations = load_expectation_suite(suite_module)
    
    logger.info(f"Validating table {database}.{schema}.{table_name} with suite {suite_name}")
    
    # Create GX context
    context = gx.get_context()
    
    # Create Snowflake datasource
    connection_string = get_snowflake_connection_string()
    
    # Build unique datasource name for this validation run
    datasource_name = f"snowflake_{table_name}"
    
    # Always create a fresh datasource for each validation
    datasource = context.data_sources.add_snowflake(
        name=datasource_name,
        connection_string=connection_string,
    )
    
    # Add table asset
    table_asset = datasource.add_table_asset(
        name=table_name,
        table_name=table_name,
        schema_name=schema,
    )
    
    # Create batch request and get batch
    batch_request = table_asset.build_batch_request()
    batch = table_asset.get_batch(batch_request)
    
    # Run validations
    all_passed = True
    results = []
    
    for expectation in expectations:
        try:
            result = batch.validate(expectation)
            results.append({
                "expectation": type(expectation).__name__,
                "success": result.success,
            })
            if not result.success:
                all_passed = False
                logger.warning(f"Expectation failed: {type(expectation).__name__}")
        except Exception as e:
            logger.error(f"Error running expectation {type(expectation).__name__}: {str(e)}")
            results.append({
                "expectation": type(expectation).__name__,
                "success": False,
                "error": str(e)
            })
            all_passed = False
    
    logger.info(f"Validation for {table_name}: {'PASSED' if all_passed else 'FAILED'}")
    
    if not all_passed and raise_on_failure:
        raise ValueError(f"Data quality validation failed for table: {table_name}")
    
    return {
        "table": table_name,
        "success": all_passed,
        "suite_name": suite_name,
        "results": results,
    }


def validate_raw_layer(raise_on_failure: bool = True) -> List[Dict[str, Any]]:
    """Validate all tables in the raw layer."""
    raw_tables = ["ORDERS_RAW"]
    results = []
    
    for table in raw_tables:
        try:
            result = validate_table(table, schema="RAW", raise_on_failure=raise_on_failure)
            results.append(result)
        except Exception as e:
            logger.error(f"Validation failed for {table}: {str(e)}")
            if raise_on_failure:
                raise
            results.append({"table": table, "success": False, "error": str(e)})
    
    return results


def validate_marts_layer(raise_on_failure: bool = True) -> List[Dict[str, Any]]:
    """Validate all tables in the marts/analytics layer."""
    mart_tables = ["dim_customer", "dim_date", "dim_product", "fact_sales"]
    results = []
    
    for table in mart_tables:
        try:
            result = validate_table(table, schema="ANALYTICS", raise_on_failure=raise_on_failure)
            results.append(result)
        except Exception as e:
            logger.error(f"Validation failed for {table}: {str(e)}")
            if raise_on_failure:
                raise
            results.append({"table": table, "success": False, "error": str(e)})
    
    return results


def validate_all(raise_on_failure: bool = True) -> Dict[str, List[Dict[str, Any]]]:
    """Validate all tables across all layers."""
    return {
        "raw": validate_raw_layer(raise_on_failure=raise_on_failure),
        "marts": validate_marts_layer(raise_on_failure=raise_on_failure),
    }
