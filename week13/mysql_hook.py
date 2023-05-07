from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.models import Variable


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'mysql_hook',
    default_args=default_args,
    schedule_interval='@daily',
    max_active_runs=1,
)

class MySqlExampleOperator(BaseOperator):
    
    @apply_defaults
    def __init__(
            self,
            *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def execute(self, context):
        mysql_conn_str = Variable.get('mysql_conn')
        hook = MySqlHook(mysql_conn=mysql_conn_str)
    
        # Execute the SQL query
        query = "SELECT * FROM my_table;"
        results = hook.get_records(sql=query)
        for row in results:
            print(row)

my_task = MySqlExampleOperator(
    task_id='mysql_task',
    dag=dag,
)


