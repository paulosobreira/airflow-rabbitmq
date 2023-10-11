from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import task
import pendulum
with DAG(
    dag_id="dag_hum", 
    description="Dag 1",
    start_date=pendulum.now(tz="America/Fortaleza"),
    schedule="@once",
    default_args={'owner': 'Paulo Sobreira'},
    tags=["Dag 1"]
) as dag:

    tarefa1 = BashOperator(
        task_id = "tarefa_hum",
        bash_command="echo olá do console"
    )

    @task()
    def tarefa2():
        print('olá do python')


    tarefa1 >> tarefa2()
if __name__ == "__main__":
    dag.test()