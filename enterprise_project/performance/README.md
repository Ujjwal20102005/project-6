# Performance
`tests/performance/test_latency.py` asserts /health p95 < 50ms in-process.
For load tests: `pip install locust` then run against a deployed environment and record results here.
Targets: p95 < 200ms, error rate < 0.1%, 99.9% availability.
