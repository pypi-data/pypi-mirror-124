"""
conftest.py according to pytest docs:
https://docs.pytest.org/en/2.7.3/plugins.html?highlight=re#conftest-py-plugins
"""
import time
import random
import pytest
from uuid import uuid4
from testcontainers.core.container import DockerContainer

from energytt_platform.models.tech import Technology, TechnologyType
from energytt_platform.bus import (
    MessageBroker,
    Message,
    messages as m,
    get_default_broker,
)


# -- Fixtures ----------------------------------------------------------------


@pytest.fixture(scope='function')
def kafka_container():
    """
    TODO
    """
    kafka_docker = DockerContainer('landoop/fast-data-dev:latest')
    kafka_docker.env.update({'ADV_HOST': 'localhost'})
    kafka_docker.ports.update({
        2181: 2181,
        3030: 3030,
        8081: 8081,
        8082: 8082,
        8083: 8083,
        9581: 9581,
        9582: 9582,
        9583: 9583,
        9584: 9584,
        9585: 9585,
        9092: 9092,
    })

    with kafka_docker as container:
        time.sleep(5)
        yield container


@pytest.fixture(scope='function')
def broker(kafka_container: DockerContainer) -> MessageBroker:
    """
    TODO
    """
    return _create_test_broker(kafka_container)


@pytest.fixture(scope='function')
def broker2(kafka_container: DockerContainer) -> MessageBroker:
    """
    TODO
    """
    return _create_test_broker(kafka_container)


@pytest.fixture(scope='function')
def msg1() -> Message:
    """
    TODO
    """
    return m.TechnologyUpdate(
        technology=Technology(
            tech_code=str(uuid4()),
            fuel_code=str(uuid4()),
            type=random.choice(list(TechnologyType)),
        ),
    )


@pytest.fixture(scope='function')
def msg2() -> Message:
    """
    TODO
    """
    return m.TechnologyUpdate(
        technology=Technology(
            tech_code=str(uuid4()),
            fuel_code=str(uuid4()),
            type=random.choice(list(TechnologyType)),
        ),
    )


@pytest.fixture(scope='function')
def msg3() -> Message:
    """
    TODO
    """
    return m.TechnologyUpdate(
        technology=Technology(
            tech_code=str(uuid4()),
            fuel_code=str(uuid4()),
            type=random.choice(list(TechnologyType)),
        ),
    )


# -- Helpers -----------------------------------------------------------------


def _create_test_broker(kafka_container: DockerContainer) -> MessageBroker:
    """
    Creates a new message broker instance with a unique Consumer Group ID.
    """
    host = kafka_container.get_container_host_ip()
    port = kafka_container.get_exposed_port(9092)
    server = f'{host}:{port}'

    return get_default_broker(
        group=str(uuid4()),
        servers=[server],
    )
