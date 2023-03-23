docker rm -f mysql 
docker rm -f django 
docker rm -f phpmyadmin 
docker rmi django:4.0 
docker-compose up -d
docker-compose ps