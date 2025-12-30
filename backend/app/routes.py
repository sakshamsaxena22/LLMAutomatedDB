from fastapi import APIRouter, HTTPException
from typing import Any, Dict, List

from app.llm import generate_query
from app.validator import validate
from app.database import collection
from app.models import QueryRequest, QueryResponse
from app.config import MAX_RESULTS

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query_transactions(payload: QueryRequest):
    # 1. Basic request validation
    if not payload.query or not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        # 2. Ask LLM to generate MongoDB query
        llm_response: Dict[str, Any] = generate_query(payload.query)

        # 3. Validate generated MongoDB query
        validate(llm_response)

        # 4. Extract MongoDB parts safely
        mongo_filter: Dict[str, Any] = llm_response.get("filter", {})
        projection: Dict[str, Any] | None = llm_response.get("projection")
        sort: List[Any] = llm_response.get("sort", [])

        # 5. Execute MongoDB query correctly
        cursor = collection.find(mongo_filter, projection)

        if sort:
            cursor = cursor.sort(sort)

        results: List[Dict[str, Any]] = list(cursor.limit(MAX_RESULTS))

        # 6. Convert ObjectId → string for JSON serialization
        for doc in results:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])

        # 7. Return structured API response
        return {
            "generated_query": llm_response,
            "count": len(results),
            "results": results,
            "raw_response": llm_response,
        }

    except HTTPException:
        # Re-raise FastAPI errors as-is
        raise

    except Exception as exc:
        # Catch unexpected runtime errors
        raise HTTPException(
            status_code=400,
            detail=f"Query execution failed: {exc}"
        )
