# KaryaPath FastAPI Application

A basic FastAPI application with a healthcheck endpoint.

## Setup

1. Install Poetry (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

## Running the Application

### Using Docker Compose
```bash
docker-compose up
```

### Running Locally
1. Install dependencies:
   ```bash
   poetry install
   ```

2. Run the application:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

## Testing

### Running Tests Locally
```bash
poetry run pytest
```

### Continuous Integration
Tests are automatically run on GitHub Actions:
- On every push to the `main` branch
- On every pull request to the `main` branch

You can view the test results in the "Actions" tab of the GitHub repository.

## API Endpoints

- `GET /healthcheck`: Returns 200 OK with status message if the application is running

## Development
The application will be available at http://localhost:8000

## Managing Dependencies

- Add a new dependency:
  ```bash
  poetry add package-name
  ```

- Add a development dependency:
  ```bash
  poetry add --group dev package-name
  ```

- Update dependencies:
  ```bash
  poetry update
  ```