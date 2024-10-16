# Define directories
SERVER_DIR=./server

# Install dependencies
install:
	poetry install

# Run the FastAPI app
run-app:
	poetry run bash -c 'PYTHONPATH=$(SERVER_DIR)/src uvicorn server.src.main:app --reload'

# Haven't tested this.
run-ingestion-and-build-db: build-db
	poetry run python $(SERVER_DIR)/src/ingestion/pipeline.py

# Download the paper metadata from arixv using the public API.
download-data:
	poetry run python $(SERVER_DIR)/src/ingestion/arxiv_client.py

# Note that the below is ingestion of the downloaded jsons, not downloading of arxiv data.
# Note that this will trigger a download of hugging face embedding models if not already cached. TODO: replace with Bedrock.
run-ingestion:
	poetry run python $(SERVER_DIR)/src/ingestion/pipeline.py

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

# Build the postgres db - don't run inside the devctontainer ... TODO: build logic to check if I'm in devcontainer.
build-db:
	 docker compose --env-file .env -f deploy/docker/postgres/docker-compose.yaml up --build

remove-db:
	docker compose --env-file .env -f deploy/docker/postgres/docker-compose.yaml down
	rm -rf deploy/docker/postgres/data

# TODO: Fix the fact I need to build-db outside the dev container and then run other commands inside it.
# deploy-local: donwload-data run-ingestion run-app
# 	echo "Local deployment complete. Run 'make remove-db' to clean up the database."
