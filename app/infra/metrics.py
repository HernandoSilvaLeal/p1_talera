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

orders_created_total = Counter(
    "orders_created_total",
    "Total number of created orders.",
)

state_transitions_total = Counter(
    "state_transitions_total",
    "Total number of state transitions.",
    ["from_status", "to_status"],
)