import json
from airflow import DAG, Dataset
from airflow.decorators import task
from datetime import datetime

# Define the datasets
my_file = Dataset('/tmp/my_file1.txt')

with DAG(
    dag_id='consumer_1',
    start_date=datetime(2024, 8, 11),
    schedule=[my_file],
    catchup=False,
    tags=['Omkar']
) as dag:

    @task
    def process_dataset():
        try:
            with open(my_file.uri, mode='r') as f:
                data = json.load(f)
                print(f"Processing data: {data}")
        except Exception as e:
            print(f"Error processing dataset: {e}")

    process_dataset()
