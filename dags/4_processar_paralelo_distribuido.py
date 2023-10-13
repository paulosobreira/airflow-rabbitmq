from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.decorators import task
import pendulum,pika,json,time,redis
with DAG(
    dag_id="4_processar_paralelo_distribuido", 
    description="Processamento paralelo distribuido",
    start_date=pendulum.datetime(2023, 10, 12, 00, 00, 00, tz="America/Fortaleza"),
    catchup=False,
    schedule="@once",
    default_args={'owner': 'Paulo Sobreira'},
    tags=["processar","paralelo","distribuido"]
) as dag:

    rabbitmq = "amqp://guest:guest@rabbitmq/"

    def verifica_processar(**kwargs):
        message = None
        connection = pika.BlockingConnection(pika.URLParameters(rabbitmq))
        channel = connection.channel()
        method_frame, _, body = channel.basic_get('queue-receber')
        if method_frame:
            message = body.decode()
            json_recebido = json.loads(message)
            salva_json(json_recebido=json_recebido,run_id=kwargs['dag_run'].run_id)
            if("processar" in json_recebido):
                returno = 'processar'
            else:
                returno = 'erro'
            channel.basic_ack(method_frame.delivery_tag)
        else:
            returno = 'fila_vazia'
        channel.close()
        connection.close()  
        return returno  

    @task
    def erro(**kwargs):
        connection = pika.BlockingConnection(pika.URLParameters(rabbitmq))
        channel = connection.channel()        
        json_recebido = busca_json(run_id=kwargs['dag_run'].run_id)
        json_recebido.update({"erros": []})
        json_recebido['erros'].append('JSON nao contem o campo processar')
        json_recebido.update({"erros": list(set(json_recebido['erros']))})     
        channel.basic_publish(
            exchange='exchanger',
            routing_key='route-erro',
            body=json.dumps(json_recebido)
        )       
        channel.close()
        connection.close()  

    @task
    def processar(**kwargs):
        json_recebido = busca_json(run_id=kwargs['dag_run'].run_id)
        print('Inicio procesasmento continuo de {} segundos '.format(json_recebido['processar']))
        time.sleep(json_recebido['processar'])
        print('Fim procesasmento continuo de {} segundos '.format(json_recebido['processar']))        

    def salva_json(json_recebido,run_id):
        r = redis.Redis(host='redis', port=6379)
        r.set(run_id+'/json_recebido', json.dumps(json_recebido))
        print(json_recebido)

    def busca_json(run_id):
        r = redis.Redis(host='redis', port=6379)
        json_recebido = json.loads(r.get(run_id+'/json_recebido'))
        print(json_recebido)
        return json_recebido 
 
    inicio = EmptyOperator(task_id="inicio", dag=dag)
    fila_vazia = EmptyOperator(task_id="fila_vazia", dag=dag)
    fim = EmptyOperator(trigger_rule='one_success',task_id="fim", dag=dag)
    verifica_processar = BranchPythonOperator(trigger_rule='one_success',task_id='verifica_processar', dag=dag ,python_callable=verifica_processar)

    inicio >> verifica_processar >> [processar(),erro(),fila_vazia] >> fim