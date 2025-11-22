from airflow import DAG
from datetime import datetime
from airflow.providers.snowflake.transfers.s3_to_snowflake import S3ToSnowflakeOperator

with DAG(
    dag_id="s3_to_snowflake_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
):

    load_to_snowflake = S3ToSnowflakeOperator(
        task_id="load_csv_s3_to_snowflake",
        snowflake_conn_id="snowflake_default",
        s3_keys=["data.csv"],  # path inside the bucket
        table="ORDERS_RAW",
        schema="RAW",
        stage="my_s3_stage",file_format="my_csv_format",    
    )
