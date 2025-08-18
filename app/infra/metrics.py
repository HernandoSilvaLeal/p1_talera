# Prometheus metrics definitions
from prometheus_client import Counter, Histogram

request_latency_seconds = Histogram(
    "request_latency_seconds",
    "Request latency in seconds.",
    ["method", "path", "status_code"],
)

requests_total = Counter(
    "requests_total",
    "Total number of requests.",
    ["method", "path"],
)
