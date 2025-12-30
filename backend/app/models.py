from __future__ import annotations

from typing import Any, Dict, List
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """
    Incoming request payload for natural language queries
    """
    query: str = Field(
        ...,
        min_length=3,
        description="Natural language query from the user"
    )


class TransactionResponse(BaseModel):
    """
    Represents a single transaction record
    """
    transaction_id: str
    user_id: str
    amount: float
    currency: str
    status: str
    merchant: str
    payment_method: str
    timestamp: str


class QueryResponse(BaseModel):
    """
    API response returned to the client
    """
    generated_query: Dict[str, Any]
    count: int
    results: List[Dict[str, Any]]
