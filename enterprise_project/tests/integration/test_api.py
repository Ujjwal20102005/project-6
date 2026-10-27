def test_health(client):
    assert client.get("/health").json()["status"] == "healthy"


def test_metrics(client):
    client.get("/health")
    assert "http_requests_total" in client.get("/metrics").text


def test_register_login_duplicate_and_bad_creds(client):
    body = {"email": "a@b.com", "password": "password123"}
    assert client.post("/auth/register", json=body).status_code == 201
    assert client.post("/auth/register", json=body).status_code == 409
    assert client.post("/auth/login", json=body).status_code == 200
    bad = client.post("/auth/login", json={"email": "a@b.com", "password": "nope"})
    assert bad.status_code == 401
    assert client.post("/auth/register", json={"email": "bad", "password": "password123"}).status_code == 422


def test_auth_required_and_roles(client, customer, admin):
    p = {"name": "Pen", "price": 10, "stock": 5}
    assert client.post("/products", json=p).status_code in (401, 403)
    assert client.post("/products", json=p, headers={"Authorization": "Bearer bad"}).status_code == 401
    assert client.post("/products", json=p, headers=customer).status_code == 403
    assert client.post("/products", json=p, headers=admin).status_code == 201
    assert len(client.get("/products?limit=10").json()) == 1


def test_order_flow(client, customer, admin):
    pid = client.post("/products", json={"name": "Pen", "price": 10.5, "stock": 5}, headers=admin).json()["id"]
    r = client.post("/orders", json={"items": [{"product_id": pid, "quantity": 2}]}, headers=customer)
    assert r.status_code == 201 and r.json()["total"] == 21.0
    assert client.get("/products").json()[0]["stock"] == 3
    assert len(client.get("/orders", headers=customer).json()) == 1


def test_order_errors(client, customer, admin):
    pid = client.post("/products", json={"name": "Pen", "price": 1, "stock": 1}, headers=admin).json()["id"]
    assert client.post("/orders", json={"items": [{"product_id": pid, "quantity": 5}]}, headers=customer).status_code == 409
    assert client.post("/orders", json={"items": [{"product_id": 999, "quantity": 1}]}, headers=customer).status_code == 404
    assert client.post("/orders", json={"items": []}, headers=customer).status_code == 422


def test_rate_limit(client, monkeypatch):
    from src.config.settings import settings
    monkeypatch.setattr(settings, "RATE_LIMIT_PER_MIN", 3)
    codes = [client.get("/health").status_code for _ in range(10)]
    assert 429 in codes


def test_storefront_served(client):
    r = client.get("/")
    assert r.status_code == 200 and "Storefront" in r.text
