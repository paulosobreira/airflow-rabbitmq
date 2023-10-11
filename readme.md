Construir imagem airflow com dependencias:
```
docker build . --tag sowbreira/airflow:2.7.1
```
Subir imagem airflow com dependencias para dockerhub:
```
docker push sowbreira/airflow:2.7.1
```
Iniciar o airflow via docker:
```
docker compose up
```
Parar o airflow via docker:
```
docker compose down
```
Parar e limpar o airflow via docker:
```
docker compose down --volumes --rmi all
```