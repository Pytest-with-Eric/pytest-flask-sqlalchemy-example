# Pytest Flask SQLAlchemy Example

## Description

This repository contains the example code for the article series on [3 Proven Ways To Test Your Flask Applications With Pytest](https://pytest-with-eric.com/api-testing/pytest-flask-postgresql-testing/)


## Installation

To install the project, you need to have Poetry installed. If you don't have it installed, you can install it by following the instructions [here](https://python-poetry.org/docs/#installation).

## Requirements
- Python 3.12
- Poetry

## Usage

### How To Run the Server

To run the server, use the following command:

```shell
$ poetry run python user_manager/app.py
```

This will spin up the server at `http://localhost:5000`

### How To Run the Tests

To run the tests, use the following command:

```shell
$ poetry run pytest
$ poetry run pytest --dburl=postgresql://myuser:mypassword@localhost:5433/mydatabase_test
```

Please follow further instructions on how to run the app in the [blog post](https://pytest-with-eric.com/api-testing/pytest-flask-postgresql-testing/).

If you have any questions about the project please raise an Issue on GitHub.