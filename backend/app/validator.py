ALLOWED_FIELDS = {
    "transaction_id",
    "user_id",
    "amount",
    "currency",
    "status",
    "merchant",
    "payment_method",
    "timestamp",
    "error_message",
}

ALLOWED_TOP_LEVEL_KEYS = {
    "filter",
    "projection",
    "sort",
    "limit",
    "pipeline",
}

DISALLOWED_OPERATORS = {
    "$where",
    "$expr",
    "$function",
    "$lookup",
    "$facet",
    "$graphLookup",
    "$merge",
    "$out",
}


def _check(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in DISALLOWED_OPERATORS:
                raise ValueError(f"Unsafe operator detected: {k}")
            _check(v)

    elif isinstance(obj, list):
        for item in obj:
            _check(item)


def validate(query: dict):
    if not isinstance(query, dict):
        raise ValueError("Query must be a JSON object")

    for key in query:
        if key not in ALLOWED_TOP_LEVEL_KEYS:
            raise ValueError(f"Unsafe top-level key: {key}")

    _check(query)
