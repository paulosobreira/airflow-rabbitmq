
from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
import pika,pendulum

with DAG(
    "1_setup_rabbitmq", 
    start_date=pendulum.now(tz="America/Fortaleza"),
    schedule=None,
    max_active_runs = 1,
    catchup=False,
    description="Setup RabbitMQ",
    default_args={'owner': 'Paulo Sobreira'},
    tags=["Setup","RabbitMQ"]
) as dag:
        
    @task()
    def setup():
        connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@rabbitmq/"))
        channel = connection.channel()    
        channel.exchange_declare(
            exchange='exchanger'
        )

        channel.queue_declare(queue='queue-receber')

        channel.queue_declare(queue='queue-erro')

        channel.queue_bind(queue='queue-receber',exchange='exchanger',routing_key='route-receber')

        channel.queue_bind(queue='queue-erro',exchange='exchanger',routing_key='route-erro')

        connection.close()

    setup()
