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