import time


def test_health_p95_under_50ms(client):
    samples = []
    for _ in range(50):
        t = time.perf_counter()
        client.get("/health")
        samples.append(time.perf_counter() - t)
    samples.sort()
    assert samples[int(len(samples) * 0.95)] < 0.05
