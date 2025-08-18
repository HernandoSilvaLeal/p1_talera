from contextvars import ContextVar, Token
from typing import Any, Optional

# Context variables
_request_id: ContextVar[Optional[str]] = ContextVar("request_id", default=None)
_order_id: ContextVar[Optional[str]] = ContextVar("order_id", default=None)
_customer_id: ContextVar[Optional[str]] = ContextVar("customer_id", default=None)

# --- Setters ---
def set_request_id(value: str) -> Token:
    return _request_id.set(value)

def set_order_id(value: str) -> Token:
    return _order_id.set(value)

def set_customer_id(value: str) -> Token:
    return _customer_id.set(value)

# --- Getters ---
def get_request_id() -> Optional[str]:
    return _request_id.get()

# --- Clear ---
def clear_context() -> None:
    _request_id.set(None)
    _order_id.set(None)
    _customer_id.set(None)