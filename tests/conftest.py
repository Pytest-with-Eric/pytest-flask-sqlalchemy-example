import pytest
import random
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool
from user_manager.app import create_app, db


def pytest_addoption(parser):
    parser.addoption(
        "--dburl",  # For Postgres use "postgresql://user:password@localhost/dbname"
        action="store",
        default="sqlite:///:memory:",  # Default uses SQLite in-memory database
        help="Database URL to use for tests.",
    )


@pytest.fixture(scope="session")
def db_url(request):
    """Fixture to retrieve the database URL."""
    return request.config.getoption("--dburl")


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
def app(db_url):
    """Session-wide test 'app' fixture."""
    test_config = {
        "SQLALCHEMY_DATABASE_URI": db_url,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
    app = create_app(test_config)

    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture(scope="function")
def session(app):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()  # Rollback any changes made during the test
    connection.close()


@pytest.fixture
def test_client(app, session):
    """Test client for the app."""
    return app.test_client()


@pytest.fixture
def user_payload():
    suffix = random.randint(1, 100)
    return {
        "username": f"JohnDoe_{suffix}",
        "email": f"john_{suffix}@doe.com",
    }
