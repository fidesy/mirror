
build:
	sudo docker build -t web-mirror .

run:
	sudo docker run --name web-mirror -dp 8000:8000 web-mirror

rundb:
	sudo docker run --name mirrordb -e POSTGRES_USER=devusermc -e POSTGRES_PASSWORD=po2O4NJH2hjoiqER -e POSTGRES_DB=posts -dp 5432:5432 postgres

remove:
	sudo docker rm -f web-mirror
	sudo docker rmi web-mirror

restart: remove build run

