run-backend:
	uvicorn app.main:app --reload

run-worker:
	python3.11 -m app.worker.server

generate-proto:
	python3.11 -m grpc_tools.protoc \
		-I./app/worker/grpc \
		--python_out=./app/worker/grpc \
		--grpc_python_out=./app/worker/grpc \
		--pyi_out=./app/worker/grpc \
		 scheduler.proto \