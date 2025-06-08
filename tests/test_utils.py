import pytest
from utils import calculate_cpa, merge_data


def test_cpa_calculation_normal():
    merged = [
        {"date": "2025-06-01", "campaign_id": "C1", "spend": 100, "conversions": 10}
    ]
    calculated = calculate_cpa(merged)
    assert calculated[0]["cpa"] == 10.0


def test_cpa_calculation_zero_conversions():
    merged = [
        {"date": "2025-06-01", "campaign_id": "C1", "spend": 100, "conversions": 0}
    ]
    calculated = calculate_cpa(merged)
    assert calculated[0]["cpa"] is None


def test_merge_data_full_match():
    spend = [{"date": "2025-06-01", "campaign_id": "C1", "spend": 100}]
    conv = [{"date": "2025-06-01", "campaign_id": "C1", "conversions": 10}]
    merged = merge_data(spend, conv)
    assert merged == [
        {"date": "2025-06-01", "campaign_id": "C1", "spend": 100, "conversions": 10}
    ]


def test_merge_data_missing_conversion():
    spend = [{"date": "2025-06-01", "campaign_id": "C1", "spend": 100}]
    conv = []  # No conversion data
    merged = merge_data(spend, conv)
    assert merged == [
        {"date": "2025-06-01", "campaign_id": "C1", "spend": 100, "conversions": 0}
    ]


def test_merge_data_missing_spend():
    spend = []
    conv = [{"date": "2025-06-01", "campaign_id": "C1", "conversions": 5}]
    merged = merge_data(spend, conv)
    assert merged == [
        {"date": "2025-06-01", "campaign_id": "C1", "spend": 0, "conversions": 5}
    ]
