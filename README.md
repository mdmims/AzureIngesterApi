# Installing

Create and activate a Python virtual environment:

```
python3 -m venv venv
source ./venv/bin/activate
```

Install the dependencies:

`pip install -r requirements.txt`

# Running the application locally

The following are scripts that can help you get started quickly and run the app server:

- Run a development server for API: `./bin/run_dev.sh`

# Running the application through Docker

`docker-compose up`

# Testing

Testing is managed and driven through Pytest. Running instructions:
- Unit
    - `pytest --ignore=integration`
- Integration (External DB must be available)
    - `pytest tests/integration`

# CI through Github Actions

Each new commit pushed to remote is tested and linting performed through Github Actions spec [python-app.yml](.github/workflows/python-app.yml)