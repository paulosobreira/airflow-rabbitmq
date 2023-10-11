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
curl -LfO 'https://github.com/paulosobreira/airflow-rabbitmq/blob/main/docker-compose.yaml'
```

>Setar AIRFLOW_UID
```
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

>Subir os containers
```
docker compose up
```


>Url de acesso:

link_gerado_playwithdocker/*tecnet2/index.jsp*

>Usuário administrador
Login : sobreira 
Senha : sobreira

>Usuário de teste
Login : teste 
Senha : teste