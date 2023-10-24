curl --location 'localhost:3000/rabbitmq' \
--header 'Content-Type: application/json' \
--data '{
    "processar" : 60
}'
sleep 2
curl --location 'localhost:3000/rabbitmq' \
--header 'Content-Type: application/json' \
--data '{
    "processar" : 50
}'
sleep 2
curl --location 'localhost:3000/rabbitmq' \
--header 'Content-Type: application/json' \
--data '{
    "processar" : 40
}'
sleep 2
curl --location 'localhost:3000/rabbitmq' \
--header 'Content-Type: application/json' \
--data '{
    "processar" : 30
}'
sleep 2
curl --location 'localhost:3000/rabbitmq' \
--header 'Content-Type: application/json' \
--data '{
    "processar" : 20
}'
sleep 2
curl --location 'localhost:3000/rabbitmq' \
--header 'Content-Type: application/json' \
--data '{
    "processar" : 10
}'