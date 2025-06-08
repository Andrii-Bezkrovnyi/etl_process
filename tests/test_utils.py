from utils import calculate_cpa, merge_data

def test_cpa_calculation():
    merged = [{"date": "2025-06-01", "campaign_id": "C1", "spend": 100, "conversions": 10}]
    calculated = calculate_cpa(merged)
    assert calculated[0]["cpa"] == 10.0

def test_merge_data():
    spend = [{"date": "2025-06-01", "campaign_id": "C1", "spend": 100}]
    conv = [{"date": "2025-06-01", "campaign_id": "C1", "conversions": 10}]
    merged = merge_data(spend, conv)
    assert merged == [{"date": "2025-06-01", "campaign_id": "C1", "spend": 100, "conversions": 10}]
