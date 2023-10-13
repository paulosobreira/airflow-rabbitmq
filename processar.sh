curl --location 'localhost:3000/rabbitmq' \
--header 'Content-Type: application/json' \
--data '{
    "processar" : 60
}'
curl --location 'localhost:3000/rabbitmq' \
--header 'Content-Type: application/json' \
--data '{
    "processar" : 50
}'
curl --location 'localhost:3000/rabbitmq' \
--header 'Content-Type: application/json' \
--data '{
    "processar" : 40
}'
curl --location 'localhost:3000/rabbitmq' \
--header 'Content-Type: application/json' \
--data '{
    "processar" : 30
}'
curl --location 'localhost:3000/rabbitmq' \
--header 'Content-Type: application/json' \
--data '{
    "processar" : 20
}'
curl --location 'localhost:3000/rabbitmq' \
--header 'Content-Type: application/json' \
--data '{
    "processar" : 10
}'