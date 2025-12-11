from airflow import DAG
# from airflow.utils.dates import days_ago
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.providers.snowflake.transfers.s3_to_snowflake import S3ToSnowflakeOperator

import logging

logger = logging.getLogger('dag_logger')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

dag =  DAG(
    dag_id='ecommerce_dag',
    # schedule_interval=None,
    # start_date = days_ago(1)

    )


def start_job():
    logging.info("Starting the pipeline.")

def end_job():
    logger.info("All process completed.")
    



start_task = PythonOperator(
    task_id='start_job',
    python_callable=start_job,
    dag=dag
)
end_task = PythonOperator(
    task_id='end_job',
    python_callable=end_job,
    dag=dag
)

upload_to_s3_task = LocalFilesystemToS3Operator(
    task_id='upload_to_s3',
    filename="/usr/local/airflow/include/data/data.csv",
    dest_key="raw/data.csv",
    dest_bucket="ecommerce-dataops",
    aws_conn_id='aws_default', 
    dag=dag
    
)

load_to_snowflake_task = S3ToSnowflakeOperator(
        task_id="load_csv_s3_to_snowflake",
        snowflake_conn_id="snowflake_default",
        s3_keys=["data.csv"],  # path inside the bucket
        table="ORDERS_RAW",
        schema="RAW",
        stage="my_s3_stage",file_format="my_csv_format",  
        dag=dag  
    )



start_task >> upload_to_s3_task >> load_to_snowflake_task >> end_task
