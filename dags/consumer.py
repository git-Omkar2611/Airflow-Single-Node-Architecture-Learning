import json
from airflow import DAG, Dataset
from airflow.decorators import task
from airflow.utils.dates import days_ago
from airflow.utils.log.logging_mixin import LoggingMixin

# Define the datasets
my_file = Dataset('/tmp/my_file.txt')
my_file_2 = Dataset('/tmp/my_file_2.txt')

with DAG(
    dag_id='consumer',
    start_date=days_ago(1),  # Adjust start_date as needed
    schedule=[my_file,my_file_2],
    catchup=False,
    tags=['Omkar']
) as dag:

    @task
    def read_from_dataset():
        try:
            with open(my_file.uri, mode='r') as f:
                content = f.read()
                print(content)
        except Exception as e:
            LoggingMixin().log.error(f"Error reading from dataset: {e}")

    @task
    def read_from_dataset2():
        try:
            with open(my_file_2.uri, mode='r') as f:
                data = json.load(f)
                print(data)
            # Push the JSON data to XCom
            return {'json_data': data}  # Returning data with key 'json_data'
        except Exception as e:
            LoggingMixin().log.error(f"Error reading from dataset 2: {e}")
            return {'json_data': None}  # Return a default or None value on error

    @task
    def process_json_data(data):
        # Access the XCom value with the key 'json_data'
        print(f"Processing data: {data['json_data']}")

    # Define task dependencies
    content = read_from_dataset()
    json_data = read_from_dataset2()
    process_json_data(json_data)
