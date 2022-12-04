ifneq (,$(wildcard .env))
    include .env
    export
endif

run:
	make -j 2 run-backend run-worker

run-backend:
	poetry run gunicorn app.main:app --reload --bind $(HOST):$(PORT) \
	--worker-class uvicorn.workers.UvicornWorker \
	--log-level info \
	--workers $(WORKERS)

run-worker:
	poetry run python3.11 -m app.worker.server

generate-proto:
	python3.11 -m grpc_tools.protoc \
		-I./app/worker/grpc \
		--python_out=./app/worker/grpc \
		--grpc_python_out=./app/worker/grpc \
		--pyi_out=./app/worker/grpc \
		 scheduler.proto \

migrate-up:
	poetry run alembic upgrade head;

migrate-down:
	poetry run alembic downgrade $(revision);

migrate-create:
	poetry run alembic revision --autogenerate -m $(name);

migrate-history:
	poetry run alembic history;

migrate-stamp:
	poetry run alembic stamp $(revision);

compose-build:
	docker-compose -f docker/docker-compose.yml --env-file=.env build

compose-up:
	docker-compose -f docker/docker-compose.yml --env-file=.env up

vulture:
	poetry run vulture app --exclude app/worker/grpc