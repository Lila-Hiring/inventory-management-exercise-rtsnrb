import os
import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from inventory_management_exercise.db import get_session
from inventory_management_exercise.main import app
from inventory_management_exercise.models.architecture import Architecture

# Add this at the top of the file after the imports
pytestmark = pytest.mark.filterwarnings("ignore::DeprecationWarning")


# Create a single engine to be shared by both fixtures
@pytest.fixture(name="test_engine")
def test_engine_fixture():
    # Create a temporary file for the test database
    temp_db = tempfile.NamedTemporaryFile(delete=False)
    temp_db_url = f"sqlite:///{temp_db.name}"
    temp_db.close()

    engine = create_engine(temp_db_url, echo=False, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    yield engine
    SQLModel.metadata.drop_all(engine)

    # Clean up the temporary file
    os.unlink(temp_db.name)


@pytest.fixture(name="session")
def session_fixture(test_engine):
    with Session(test_engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(test_engine):
    # Create a session that will be used for both the test and the API
    test_session = Session(test_engine)

    def get_session_override():
        return test_session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client

    test_session.close()
    app.dependency_overrides.clear()


def test_list_architectures_empty(client, session):
    response = client.get("/v1/architectures")
    assert response.status_code == 200
    architectures = response.json()
    assert len(architectures) == 0


def test_get_architecture(client, session):
    arch = Architecture(name="arm64", description="64-bit ARM architecture")
    session.add(arch)
    session.commit()

    response = client.get(f"/v1/architectures/{arch.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "arm64"
    assert data["description"] == "64-bit ARM architecture"


def test_get_architecture_not_found(client):
    response = client.get("/v1/architectures/999")
    assert response.status_code == 404


def test_create_architecture(client):
    new_arch = {"name": "riscv", "description": "RISC-V architecture", "soft_deleted": False}
    response = client.post("/v1/architectures", json=new_arch)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "riscv"
    assert data["description"] == "RISC-V architecture"
    assert "id" in data


def test_update_architecture(client, session):
    # Create initial architecture
    arch = Architecture(name="mips", description="MIPS architecture")
    session.add(arch)
    session.commit()

    # Update the architecture
    updated_data = {"name": "mips64", "description": "64-bit MIPS architecture", "soft_deleted": False}
    response = client.put(f"/v1/architectures/{arch.id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "mips64"
    assert data["description"] == "64-bit MIPS architecture"


def test_update_architecture_not_found(client):
    updated_data = {"name": "invalid", "description": "This should fail", "soft_deleted": False}
    response = client.put("/v1/architectures/999", json=updated_data)
    assert response.status_code == 404


def test_soft_delete_architecture(client, session):
    # Create architecture to delete
    arch = Architecture(name="powerpc", description="PowerPC architecture")
    session.add(arch)
    session.commit()

    # Soft delete the architecture
    response = client.delete(f"/v1/architectures/{arch.id}")
    assert response.status_code == 200

    # Verify it's not in the list anymore
    response = client.get("/v1/architectures")
    assert response.status_code == 200
    architectures = response.json()
    assert not any(a["id"] == arch.id for a in architectures)


def test_soft_delete_architecture_not_found(client):
    response = client.delete("/v1/architectures/999")
    assert response.status_code == 404
