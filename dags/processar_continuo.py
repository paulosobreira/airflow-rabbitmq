from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.decorators import task
import pendulum,pika,json,time,pickle,os,shutil
with DAG(
    dag_id="processar_continuo", 
    description="Processamento continuo",
    start_date=pendulum.datetime(2023, 10, 12, 00, 00, 00, tz="America/Fortaleza"),
    catchup=False,
    schedule="@continuous",
    max_active_runs = 1,
    default_args={'owner': 'Paulo Sobreira'},
    tags=["processar","continuo"]
) as dag:

    rabbitmq = "amqp://guest:guest@rabbitmq/"

    @task
    def inicio():
        if os.path.isdir(dag.dag_id):
            shutil.rmtree(dag.dag_id)
        os.mkdir(dag.dag_id)         
    
    def verifica_processar():
        message = None
        connection = pika.BlockingConnection(pika.URLParameters(rabbitmq))
        channel = connection.channel()
        method_frame, _, body = channel.basic_get('queue-receber')
        if method_frame:
            message = body.decode()
            json_recebido = json.loads(message)
            salva_json(json_recebido=json_recebido,dag=dag)
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
    def erro():
        connection = pika.BlockingConnection(pika.URLParameters(rabbitmq))
        channel = connection.channel()        
        json_recebido = busca_json(dag=dag)
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
    def processar():
        json_recebido = busca_json(dag=dag)
        print('Inicio procesasmento continuo de {} segundos '.format(json_recebido['processar']))
        time.sleep(json_recebido['processar'])
        print('Fim procesasmento continuo de {} segundos '.format(json_recebido['processar']))        

    def salva_json(json_recebido,dag):
        with open(dag.dag_id+'/json_recebido', 'wb') as f:
            pickle.dump(json_recebido, f, pickle.HIGHEST_PROTOCOL)        
        print(json_recebido)   

    def busca_json(dag):
        with open(dag.dag_id+'/json_recebido', 'rb') as f:
            json_recebido = pickle.load(f)
        print(json_recebido)
        return json_recebido 
 
    fila_vazia = EmptyOperator(task_id="fila_vazia", dag=dag)
    fim = EmptyOperator(trigger_rule='one_success',task_id="fim", dag=dag)
    verifica_processar = BranchPythonOperator(trigger_rule='one_success',task_id='verifica_processar', dag=dag ,python_callable=verifica_processar)

    inicio() >> verifica_processar >> [processar(),erro(),fila_vazia] >> fim