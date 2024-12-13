import os
import pytest

os.environ["__USE_MEMORY_DB"] = "1"

from dhondt.web.app import create_app
from dhondt.db.controller import get_db_session


@pytest.fixture
def db_session():
    with get_db_session() as session:
        yield session


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
