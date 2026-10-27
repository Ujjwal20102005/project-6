import os
import tempfile

_db = os.path.join(tempfile.mkdtemp(), "test.db")
os.environ["DATABASE_URL"] = f"sqlite:///{_db}"
os.environ["RATE_LIMIT_PER_MIN"] = "100000"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from src.core.database import Base, SessionLocal, engine  # noqa: E402
from src.main import app  # noqa: E402
from src.services.services import UserService  # noqa: E402


@pytest.fixture()
def client():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return TestClient(app)


def _token(client, email, role="customer"):
    db = SessionLocal()
    UserService(db).register(email, "password123", role)
    db.close()
    r = client.post("/auth/login", json={"email": email, "password": "password123"})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture()
def admin(client):
    return _token(client, "admin@x.com", "admin")


@pytest.fixture()
def customer(client):
    return _token(client, "cust@x.com")
