from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.decorators import task
import pendulum,pika,json,time
with DAG(
    dag_id="2_processar_paralelo", 
    description="Processamento em paralelo",
    start_date=pendulum.now(tz="America/Fortaleza"),
    schedule="@once",
    default_args={'owner': 'Paulo Sobreira'},
    tags=["processar","paralelo"]
) as dag:

    @task()
    def processar():
        message = None
        connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@rabbitmq/"))
        channel = connection.channel()
        method_frame, _, body = channel.basic_get('queue-receber')
        if method_frame:
            message = body.decode()
            json_recebido = json.loads(message)
            if("processar" in json_recebido):
                print('Inicio procesasmento de {} segundos '.format(json_recebido['processar']))
                time.sleep(json_recebido['processar'])
                print('Fim procesasmento de {} segundos '.format(json_recebido['processar']))
            else:
                json_recebido.update({"erros": []})
                json_recebido['erros'].append('JSON nao contem o campo processar')
                json_recebido.update({"erros": list(set(json_recebido['erros']))})     
                channel.basic_publish(
                    exchange='exchanger',
                    routing_key='route-erro',
                    body=json.dumps(json_recebido)
                )
            channel.basic_ack(method_frame.delivery_tag)
        channel.close()
        connection.close()                
 
    inicio = EmptyOperator(task_id="inicio", dag=dag)
    fim = EmptyOperator(task_id="fim", dag=dag)

    inicio >> processar() >> fim