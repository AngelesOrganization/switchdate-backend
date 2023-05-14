import time
from typing import Any, Optional
from typing import Generator

import docker
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main.commons.db_configuration import Base
from src.main.commons.db_configuration import get_db
from src.main.commons.main import api_router
from src.test.config import settings


def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


engine = create_engine(settings.DATABASE_URL_TEST)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
        app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


class PostgresImage:
    _container_id: Optional[str] = None
    _container_obj: Optional[docker.models.containers.Container] = None
    _docker_client: docker.client.DockerClient

    def __init__(self):
        self._docker_client = docker.from_env()

    def _wait_until_created(self, tries=10, sleep_seconds=1) -> None:
        for _ in range(tries):
            try:
                self._container_obj = self._docker_client.containers.get(self._container_id)
            except docker.errors.NotFound:
                time.sleep(sleep_seconds)
                continue
            else:
                break
        else:
            raise Exception("Container not created")

    def _check_ready(self, tries=30, sleep_seconds=1) -> None:
        ready = False
        for _ in range(tries):
            # Consider the container ready when 'database system is ready to accept connections' is seen AFTER a
            # 'listening on IPv4 address "0.0.0.0", port 5432' line. Those before that are initialization by the image's
            # entrypoint scripts.
            found_network_activated_line = False
            for line in self._container_obj.logs().decode('utf-8').splitlines():
                if 'listening on IPv4 address' in line:
                    found_network_activated_line = True
                if found_network_activated_line and 'database system is ready to accept connections' in line:
                    ready = True
                    break
            if ready:
                break
            else:
                time.sleep(sleep_seconds)
                continue
        else:
            raise Exception("Container not ready within timeout")

    def run(self):
        container_image = "postgres:13"
        image_options = dict(
            mem_limit='1g',
            environment={
                "POSTGRES_PASSWORD": "example",
                "POSTGRES_DB": "postgres",
                "POSTGRES_USER": "postgres",
            },
            ports={"5432/tcp": ("127.0.0.1", 65432)},
            privileged=False,
            detach=True,
            tmpfs=["/var/lib/postgresql/data"],  # No persistence required, create tempdir in memory.
            remove=True,  # clean up container after it has run
        )
        container = self._docker_client.containers.run(container_image, **image_options)
        self._container_id = container.id
        self._wait_until_created()
        self._check_ready()
        return self._container_obj.attrs['NetworkSettings']['IPAddress']

    def stop(self):
        if self._container_id is None:
            return
        try:
            self._wait_until_created()  # In case it's stopped while it was still creating.
        except:
            return
        try:
            self._container_obj.kill()
        except docker.errors.APIError:
            pass


@pytest.fixture(scope='session')
def postgres_container() -> str:
    postgres_image = PostgresImage()
    host = postgres_image.run()
    yield "postgresql://postgres:example@%s/postgres" % host
    postgres_image.stop()
