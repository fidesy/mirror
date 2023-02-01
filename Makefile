
build:
	docker build -t web-mirror .

run:
	docker run --name web-mirror -dp 8000:8000 web-mirror

rundb:
	docker run --name mirrordb -e POSTGRES_USER=devusermc -e POSTGRES_PASSWORD=po2O4NJH2hjoiqER -e POSTGRES_DB=posts -dp 19812:5432 postgres

remove:
	docker rm -f web-mirror
	docker rmi web-mirror

restart: remove build run

