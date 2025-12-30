from typing import Any, Dict, List
from pydantic import BaseModel, Field
from app.security import Role


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3)
    role: Role = Role.viewer


class QueryResponse(BaseModel):
    generated_query: Dict[str, Any]
    count: int
    results: List[Dict[str, Any]]
    raw_response: Dict[str, Any]
