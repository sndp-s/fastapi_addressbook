"""
Utilities for standard API response strcutures
"""

from typing import Any, Dict, Optional
from fastapi import status
from fastapi.responses import JSONResponse

def create_response(
        data: Optional[Dict[str, Any]] = None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK
    ) -> JSONResponse:
    """
    Standard success response
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success",
            "message": message,
            "data": data or {}
        }
    )

def create_error_response(
        message: str = "Error",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        data: Optional[Dict[str, Any]] = None
    ) -> JSONResponse:
    """
    Standard error response
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message,
            "data": data or {}
        }
    )
