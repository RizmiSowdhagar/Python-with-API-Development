from app.services.report_service import build_usage_summary


class DummyCalc:
    def __init__(self, operation):
        # we only care that it has either .operator or .operation
        self.operation = operation


def test_build_usage_summary_counts_operations():
    calcs = [
        DummyCalc("add"),
        DummyCalc("add"),
        DummyCalc("subtract"),
    ]

    summary = build_usage_summary(calcs)

    assert summary.total_calculations == 3

    op_counts = {item.operator: item.count for item in summary.per_operation}
    # 2 adds, 1 subtract
    assert op_counts["add"] == 2
    assert op_counts["subtract"] == 1
