
run:
	python -m uvicorn mirror.main:app --reload

rundb:
	docker run --name tgdb -e POSTGRES_PASSWORD=postgres -dp 5432:5432 postgres

connect:
	docker exec -it tgdb bash -c 'psql -U postgres'
	
migrate-up: 
	migrate -source file:migrations -database 'postgres://postgres:postgres@localhost?sslmode=disable' -verbose up

migrate-down: 
	migrate -source file:migrations -database 'postgres://postgres:postgres@localhost?sslmode=disable' -verbose down

add:
	curl -X POST -H "X-TOKEN: secret_token" http://localhost:8000/api/channel?username=some_username