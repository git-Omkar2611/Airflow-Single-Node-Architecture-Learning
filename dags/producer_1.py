import json
from airflow import DAG, Dataset
from airflow.decorators import task
from datetime import datetime
from tempfile import NamedTemporaryFile
import shutil

# Define the datasets
my_file = Dataset('/tmp/my_file1.txt')
staging_file_prefix = '/tmp/staging_file_'

with DAG(
    dag_id='producer_1',
    start_date=datetime(2024, 8, 11),
    schedule='@daily',
    catchup=False,
    tags=['Omkar']
) as dag:

    @task(outlets=[my_file])
    def update_dataset(data,part_number):
        # Write to a staging file first
        staging_file = f'{staging_file_prefix}{part_number}.json'
        with open(staging_file, mode='w') as f:
            json.dump(data, f)
        
        # Move staging file to the final dataset location
        shutil.move(staging_file, my_file.uri)

    # Example tasks
    data1 = {"key1": "value1"}
    data2 = {"key2": "value2"}

    update_dataset(data1,1)
    update_dataset(data2,2)
