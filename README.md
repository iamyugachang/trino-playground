# trino-playground

## Description

This project is a data platform playground that demonstrates the integration of Trino with PostgreSQL and MongoDB. It showcases how to query data from multiple sources and perform cross-database queries using Trino.

## Features

- **Data Initialization**: Scripts to populate PostgreSQL and MongoDB with sample data.
- **Trino Configuration**: Pre-configured Trino setup for querying PostgreSQL and MongoDB.
- **Cross-Database Queries**: Example queries that combine data from PostgreSQL and MongoDB.
- **Dockerized Environment**: Easy setup using Docker Compose.

## Installation

1. Install [Poetry](https://python-poetry.org/docs/#installation) if you don't have it already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install the project dependencies:
   ```bash
   poetry install
   ```

3. Activate the virtual environment:
   ```bash
   eval $(poetry env info --path)/bin/activate
   ```

## Usage

1. Access the Trino web interface at [http://localhost:8080](http://localhost:8080).

2. Run the query test script:
   ```bash
   python trino_query_test.py
   ```

3. Modify and experiment with the provided Trino queries in `trino_query_test.py`.

## Project Structure

- `data_init.py`: Script to initialize PostgreSQL and MongoDB with sample data.
- `trino_query_test.py`: Script to test Trino queries.
- `docker-compose.yml`: Docker Compose file to set up PostgreSQL, MongoDB, and Trino.
- `trino-conf/`: Configuration files for Trino.
- `pyproject.toml`: Python project dependencies.

## Structures

Below is a UML diagram representing the structure and relationships in this project:

```mermaid
classDiagram
    class Trino {
        +Query PostgreSQL
        +Query MongoDB
        +Cross-Database Queries
    }
    class PostgreSQL {
        +customers
        +products
        +orders
        +order_items
    }
    class MongoDB {
        +users
        +reviews
        +inventory
    }
    class DockerCompose {
        +PostgreSQL Service
        +MongoDB Service
        +Trino Service
    }
    Trino --> PostgreSQL : Queries
    Trino --> MongoDB : Queries
    DockerCompose --> PostgreSQL : Service
    DockerCompose --> MongoDB : Service
    DockerCompose --> Trino : Service
```

## Requirements

- Python 3.10 or higher
- Docker and Docker Compose

## License

This project is licensed under the MIT License. See the LICENSE file for details.