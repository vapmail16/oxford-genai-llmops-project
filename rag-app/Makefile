# Define directories
SERVER_DIR=./server

# Install dependencies
install:
	poetry install

# Run the FastAPI app
run:
	poetry run bash -c 'PYTHONPATH=$(SERVER_DIR)/src uvicorn server.src.main:app --reload'

# Lint the project (using Ruff)
lint:
	poetry run ruff $(SERVER_DIR)

# Format the code (using black)
format:
	poetry run black $(SERVER_DIR)

# Run tests
test:
	poetry run pytest

# Clean up build artifacts (if any)
clean:
	find . -type f -name '*.pyc' -delete

# Build the postgres db - don't run inside the devctontainer ...
build-db:
	 docker compose --env-file .env -f deploy/docker/postgres/docker-compose.yaml up --build

remove-db:
	docker compose --env-file .env -f deploy/docker/postgres/docker-compose.yaml down
	rm -rf deploy/docker/postgres/data