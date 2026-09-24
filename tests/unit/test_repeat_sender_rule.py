import pandas as pd
from aml_detector.rules.repeat_sender_rule import RepeatSenderRule


def test_flags_account_above_threshold():
    # Fake data: account A sends 25 transactions, account B sends 3
    rows = []
    for i in range(25):
        rows.append({"Account": "A", "Is Laundering": 0})
    for i in range(3):
        rows.append({"Account": "B", "Is Laundering": 0})
    # A has one laundering transaction
    rows.append({"Account": "A", "Is Laundering": 1})

    data = pd.DataFrame(rows)
    rule = RepeatSenderRule(max_transactions=20)
    result = rule.evaluate(data)

    assert len(result) == 1
    assert result.iloc[0]["account"] == "A"
    assert result.iloc[0]["total_transactions"] == 26
    assert result.iloc[0]["laundering_transactions"] == 1


def test_does_not_flag_below_threshold():
    rows = [{"Account": "B", "Is Laundering": 0} for _ in range(5)]
    data = pd.DataFrame(rows)

    rule = RepeatSenderRule(max_transactions=20)
    result = rule.evaluate(data)

    assert result.empty