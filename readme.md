# airflow-rabbitmq

Exemplo de uma arquitetura de processamento de dados com Airflow e RabbitMQ.
O JSON de dados é eviado ao RabbitMQ via WebHook e processado com uma Dag do Airflow.

Lista de tecnologias usadas:
1. Python
2. Node
3. JavaScript
4. RabbitMQ
5. Airflow
   
## Como testar

Pode ser executado no [Play with Docker](https://labs.play-with-docker.com/)

>Criar diretorio de DAGs e baixar as DAGs
```
mkdir -p ./dags ./logs ./plugins ./config
cd dags
curl -LfO 'https://raw.githubusercontent.com/paulosobreira/airflow-rabbitmq/main/dags/1_setup_rabbitmq.py'
curl -LfO 'https://raw.githubusercontent.com/paulosobreira/airflow-rabbitmq/main/dags/2_processar_paralelo.py'
curl -LfO 'https://raw.githubusercontent.com/paulosobreira/airflow-rabbitmq/main/dags/3_processar_continuo.py'
curl -LfO 'https://raw.githubusercontent.com/paulosobreira/airflow-rabbitmq/main/dags/4_processar_paralelo_distribuido.py'
cd ~
curl -LfO 'https://raw.githubusercontent.com/paulosobreira/airflow-rabbitmq/main/processar.sh'
chmod +x processar.sh
```
>Iniciar containers do Node,RabbitMQ e Airflow
```
curl -LfO 'https://raw.githubusercontent.com/paulosobreira/airflow-rabbitmq/main/docker-compose.yaml'
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
docker compose up
```
>Portas, sistemas e usuários(usuário:senha):
```
5000 Airflow airflow:airflow
15672 RabbitMQ guest:guest
3000 Web-Hook-RabbitMQ 
```
>Post JSON Web-Hook-RabbitMQ
```
curl --location 'link_gerado_playwithdocker_porta_3000/rabbitmq' \
--header 'Content-Type: application/json' \
--data '{
    "processar" : 100
}'
```
>Limpar tudo
```
docker compose down --volumes --rmi all
```