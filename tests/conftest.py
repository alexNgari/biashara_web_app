import pytest
from app import app

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app_client = app.test_client()

    # return app_client     #not cool
    ctx = app.app_context()
    ctx.push()
    yield app_client
    ctx.pop()