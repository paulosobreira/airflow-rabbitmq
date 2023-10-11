# airflow-rabbitmq

Projeto de um sistema de processamento de dados com Airflow e RabbitMQ.
O JSON de dados é eviado ao ao RabbitMQ via WebHook e processado com uma Dag do Airflow.

Lista de tecnologias usadas:
1. Python
2. Node
3. JavaScript
4. RabbitMQ
5. Airflow
   
## Como testar

Pode ser executado no [Play with Docker](https://labs.play-with-docker.com/)

>Baixar o Dokcer compose
```
curl -LfO 'https://raw.githubusercontent.com/paulosobreira/airflow-rabbitmq/main/docker-compose.yaml'
```

>Criar diretorio de DAGs
```
mkdir -p ./dags 
```

>Configurar o AIRFLOW_UID
```
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

>Inicia Airflow
```
docker compose up airflow-init
```

>Subir os containers
```
docker compose up
```
>Abrir portas:
```
5000 Airflow usuario:senha airflow:airflow
15672 RabbitMQ usuario:senha guest:guest
3000 web-hook rabbitmq 
```




>Usuário administrador
Login : sobreira 
Senha : sobreira

>Usuário de teste
Login : teste 
Senha : teste