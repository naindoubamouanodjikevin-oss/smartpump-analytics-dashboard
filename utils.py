import pandas as pd
import numpy as np
import logging
import os

# Configure logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def validate_dataframe(df):
    """Validates that the uploaded CSV contains required columns and valid ranges."""
    required_cols = ['timestamp', 'pump_id', 'flow_rate', 'head_pressure', 'power_input']
    
    # Check columns
    for col in required_cols:
        if col not in df.columns:
            logging.error(f"Missing required column: {col}")
            raise ValueError(f"Invalid CSV Structure: Missing required column '{col}'.")
            
    # Check for negative values in numeric fields
    numeric_fields = ['flow_rate', 'head_pressure', 'power_input']
    for col in numeric_fields:
        if (df[col] < 0).any():
            logging.error(f"Negative values detected in column: {col}")
            raise ValueError(f"Invalid values: Negative numbers are not allowed in '{col}'.")
            
    logging.info("CSV validation passed successfully.")
    return True

def calculate_pump_metrics(df):
    """Calculates hydraulic power and pump efficiency percentage."""
    # Constants: Water density rho = 1000 kg/m^3, gravity g = 9.81 m/s^2
    rho = 1000.0
    g = 9.81
    
    # Hydraulic Power (kW) = (Q * H * rho * g) / (3600 * 1000)
    df['hydraulic_power_kw'] = (df['flow_rate'] * df['head_pressure'] * rho * g) / 3600000.0
    
    # Efficiency (%) = (Hydraulic Power / Power Input) * 100
    df['efficiency'] = np.where(
        df['power_input'] > 0,
        (df['hydraulic_power_kw'] / df['power_input']) * 100,
        0.0
    )
    
    # Determine Health State
    conditions = [
        (df['efficiency'] >= 75.0),
        (df['efficiency'] >= 60.0) & (df['efficiency'] < 75.0),
        (df['efficiency'] < 60.0)
    ]
    choices = ['HEALTHY', 'DEGRADED', 'FAILED']
    df['health_state'] = np.select(conditions, choices, default='RECOVERING')
    
    return df
