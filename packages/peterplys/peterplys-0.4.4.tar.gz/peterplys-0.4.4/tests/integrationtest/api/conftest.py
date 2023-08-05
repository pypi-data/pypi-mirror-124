"""
conftest.py according to pytest docs:
https://docs.pytest.org/en/2.7.3/plugins.html?highlight=re#conftest-py-plugins
"""
import pytest
from datetime import datetime, timedelta, timezone

from energytt_platform.api import Application
from energytt_platform.models.auth import InternalToken
from energytt_platform.tokens import TokenEncoder


@pytest.fixture(scope='function')
def app(secret: str):
    """
    TODO
    """
    yield Application.create(
        name='Test API',
        secret=secret,
        health_check_path='/health',
    )


@pytest.fixture(scope='function')
def client(app: Application):
    """
    TODO
    """
    yield app.test_client


@pytest.fixture(scope='function')
def secret():
    """
    TODO
    """
    yield 'something secret'


@pytest.fixture(scope='function')
def token_encoder(secret: str):
    """
    TODO
    """
    yield TokenEncoder(
        schema=InternalToken,
        secret=secret,
    )


@pytest.fixture(scope='function')
def valid_token():
    """
    TODO
    """
    yield InternalToken(
        issued=datetime.now(tz=timezone.utc),
        expires=datetime.now(tz=timezone.utc) + timedelta(days=1),
        actor='foo',
        subject='bar',
        scope=['scope1', 'scope2'],
    )


@pytest.fixture(scope='function')
def valid_token_encoded(
        valid_token: InternalToken,
        token_encoder: TokenEncoder[InternalToken],
):
    """
    TODO
    """
    yield token_encoder.encode(valid_token)
