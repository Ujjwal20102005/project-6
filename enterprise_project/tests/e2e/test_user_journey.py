def test_full_journey(client, admin):
    client.post("/auth/register", json={"email": "new@x.com", "password": "password123"})
    tok = client.post("/auth/login", json={"email": "new@x.com", "password": "password123"}).json()["access_token"]
    h = {"Authorization": f"Bearer {tok}"}
    pid = client.post("/products", json={"name": "Book", "price": 300, "stock": 2}, headers=admin).json()["id"]
    order = client.post("/orders", json={"items": [{"product_id": pid, "quantity": 1}]}, headers=h).json()
    assert order["total"] == 300
