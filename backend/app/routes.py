from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

from app.llm import generate_query
from app.validator import validate
from app.database import collection
from app.models import QueryRequest, QueryResponse
from app.config import MAX_RESULTS

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query_transactions(payload: QueryRequest):
    try:
        llm_query: Dict[str, Any] = generate_query(payload.query)

        validate(llm_query)

        # 🔹 FIND QUERY
        if "filter" in llm_query:
            cursor = collection.find(
                llm_query["filter"],
                llm_query.get("projection"),
            )

            if llm_query.get("sort"):
                cursor = cursor.sort(llm_query["sort"])

            results = list(cursor.limit(llm_query.get("limit", MAX_RESULTS)))

        # 🔹 AGGREGATION QUERY
        elif "pipeline" in llm_query:
            pipeline = llm_query["pipeline"] + [{"$limit": llm_query.get("limit", MAX_RESULTS)}]
            results = list(collection.aggregate(pipeline))

        else:
            raise HTTPException(400, "Unsupported query structure")

        for doc in results:
            doc["_id"] = str(doc["_id"])

        return {
            "generated_query": llm_query,
            "count": len(results),
            "results": results,
            "raw_response": llm_query,
        }

    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
