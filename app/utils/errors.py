from typing import Any, Optional, Dict
from fastapi import status
from fastapi.responses import ORJSONResponse
from app.utils import request_context

def problem(
    status_code: int,
    message: str,
    *,
    code: Optional[str] = None,
    details: Optional[Any] = None,
) -> ORJSONResponse:
    """
    Devuelve un error con shape consistente.
    {
      "error": {
        "code": "string|None",
        "message": "string",
        "details": ..., 
        "request_id": "uuid"
      }
    }
    """
    body: Dict[str, Any] = {
        "error": {
            "code": code,
            "message": message,
            "details": details,
            "request_id": request_context.get_request_id(),
        }
    }
    return ORJSONResponse(status_code=status_code, content=body)