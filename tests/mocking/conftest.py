import pytest
import random
from user_manager.app import create_app
from user_manager.models import db


@pytest.fixture(scope="session")
def app():
    """Session-wide test 'app' fixture."""
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:postgres@localhost:5432/dummy_db",  # Dummy database URL
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
    app = create_app(test_config)
    with app.app_context():
        yield app


@pytest.fixture
def test_client(app):
    """Test client for the app."""
    return app.test_client()


@pytest.fixture
def user_payload():
    suffix = random.randint(1, 100)
    return {
        "username": f"JohnDoe_{suffix}",
        "email": f"john_{suffix}@doe.com",
    }
