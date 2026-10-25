import pytest
import pandas as pd
from utils import validate_dataframe, calculate_pump_metrics

def test_validate_dataframe_success():
    valid_data = pd.DataFrame({
        'timestamp': ['2026-10-01 08:00:00'],
        'pump_id': ['PUMP-01'],
        'flow_rate': [120.5],
        'head_pressure': [45.2],
        'power_input': [25.0]
    })
    assert validate_dataframe(valid_data) == True

def test_validate_dataframe_missing_column():
    invalid_data = pd.DataFrame({
        'timestamp': ['2026-10-01 08:00:00'],
        'pump_id': ['PUMP-01'],
        'flow_rate': [120.5]
    })
    with pytest.raises(ValueError):
        validate_dataframe(invalid_data)

def test_calculate_pump_metrics():
    test_data = pd.DataFrame({
        'timestamp': ['2026-10-01 08:00:00'],
        'pump_id': ['PUMP-01'],
        'flow_rate': [150.0],
        'head_pressure': [40.0],
        'power_input': [25.0]
    })
    result_df = calculate_pump_metrics(test_data)
    assert 'efficiency' in result_df.columns
    assert 'health_state' in result_df.columns
    assert result_df['health_state'].iloc[0] in ['HEALTHY', 'DEGRADED', 'FAILED', 'RECOVERING']
