import uuid
from starlette.requests import Request

def generate_request_id():
    """Generate a unique request ID."""
    return str(uuid.uuid4())

async def ensure_request_id(request: Request, call_next):
    """
    Ensure that a request ID is present in the request headers.
    This is a standard FastAPI middleware.
    """
    if 'X-Request-Id' not in request.headers:
        # This modification is safe as headers are mutable within the middleware scope
        request.headers.__dict__["_list"].append((b'x-request-id', generate_request_id().encode()))
    response = await call_next(request)
    return response
