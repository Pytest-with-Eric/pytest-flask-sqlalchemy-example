import pytest
import os
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool
from user_manager.app import app, db


def pytest_addoption(parser):
    parser.addoption(
        "--dburl",  # For Postgres use "postgresql://user:password@localhost/dbname"
        action="store",
        default="sqlite:///:memory:",  # Default uses SQLite in-memory database
        help="Database URL to use for tests.",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    db_url = session.config.getoption("--dburl")
    try:
        # Attempt to create an engine and connect to the database.
        engine = create_engine(
            db_url,
            poolclass=StaticPool,
        )
        connection = engine.connect()
        connection.close()  # Close the connection right after a successful connect.
        print("Database connection successful........")
    except SQLAlchemyOperationalError as e:
        print(f"Failed to connect to the database at {db_url}: {e}")
        pytest.exit(
            "Stopping tests because database connection could not be established."
        )


@pytest.fixture(scope="session")
def db_url(request):
    """Fixture to retrieve the database URL."""
    return request.config.getoption("--dburl")


# @pytest.fixture(scope="module")
# def test_client(db_url):
#     app.config["TESTING"] = True
#     app.config["SQLALCHEMY_DATABASE_URI"] = db_url

#     with app.test_client() as client:
#         with app.app_context():
#             db.create_all()
#         yield client

#     with app.app_context():
#         db.drop_all()


# @pytest.fixture
# def test_client():
#     db_fd, app.config["DATABASE"] = tempfile.mkstemp()
#     app.config["TESTING"] = True

#     with app.test_client() as client:
#         with app.app_context():
#             db.create_all()
#         yield client

#     os.close(db_fd)
#     os.unlink(app.config["DATABASE"])


@pytest.fixture
def test_client(db_url):
    app.config["DATABASE"] = db_url
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


@pytest.fixture
def user_payload():
    return {"username": "JohnDoe", "email": "john@doe.com"}
