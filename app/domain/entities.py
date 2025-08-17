from typing import Set

ALLOWED: dict[str, Set[str]] = {
    "CREATED": {"PAID", "CANCELLED"},
    "PAID": {"FULFILLED", "CANCELLED"},
    "FULFILLED": set(),
    "CANCELLED": set(),
}

def can_transition(src: str, dst: str) -> bool:
    return dst in ALLOWED.get(src, set())
