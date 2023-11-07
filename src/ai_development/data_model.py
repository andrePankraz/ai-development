"""
This file was created by ]init[ AG 2023.

Module for Data Model.
"""
from pydantic import BaseModel


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"
