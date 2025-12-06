from datetime import datetime
from collections import Counter
from typing import Iterable

from app import schemas


def _get_operator_name(calc) -> str:
    """
    Try a few possible attribute names on the Calculation model
    to figure out what the operator is.
    """
    for attr in ("operator", "operation", "operation_type", "op"):
        if hasattr(calc, attr):
            value = getattr(calc, attr)
            if value is not None:
                return str(value)
    return "unknown"


def build_usage_summary(calculations: Iterable):
    """
    calculations: iterable of Calculation objects from the DB.
    """
    calculations = list(calculations)
    total = len(calculations)

    operator_counts = Counter(_get_operator_name(c) for c in calculations)

    per_operation = [
        schemas.OperationCount(operator=op, count=count)
        for op, count in operator_counts.items()
    ]

    # Optional: last_calculation_at stays None because your model
    # does not seem to have a created_at column, and that's OK.
    last_calc = None

    return schemas.UsageSummary(
        total_calculations=total,
        per_operation=per_operation,
        last_calculation_at=last_calc,
    )
