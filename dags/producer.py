import json
from airflow import DAG , Dataset
from airflow.decorators import task

from datetime import datetime

my_file = Dataset('/tmp/my_file.txt')
my_file_2 = Dataset('/tmp/my_file_2.txt')

with DAG( dag_id =  "producer",
         start_date = datetime(2024,8,11),
         schedule ='@daily',
         catchup = False,
         tags = ['Omkar']
         ) as dag :
    
    @task(outlets = [my_file])

    def update_dataset() :
        with open(my_file.uri , mode='a+') as f :
            f.write('producer updated')

    @task(outlets = [my_file_2])
    def update_dataset2() :
        data = {"key": "value", "foo": "bar"}  # Example JSON data
        with open(my_file_2.uri , mode='w') as f :
            json.dump(data, f)

    update_dataset() >> update_dataset2()