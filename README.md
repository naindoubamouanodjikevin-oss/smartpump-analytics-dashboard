# SmartPump Analytics Dashboard

## 1. Project Overview
- **What the application does:** Analyzes industrial centrifugal pump performance, calculates operating efficiency curves, monitors power consumption, and flags cavitation risks based on time-series telemetry data.
- **What problem it solves:** Eliminates unexpected pump failures, excessive energy consumption, and manual spreadsheet errors in plant operations by providing automated real-time diagnostics.
- **What workbook or original process it replaced:** Replaced a legacy Excel workbook ("Pump_Monitoring_V2.xlsx") prone to macro corruption, broken formulas, and slow manual data entry.
- **Who the intended user is:** Plant reliability engineers, maintenance technicians, and operations supervisors.

## 2. System Requirements
- **Python Version:** Python 3.10 or higher
- **Libraries:** Streamlit, Pandas, NumPy, Plotly, Pytest (see `requirements.txt`)
- **Browser:** Google Chrome, Mozilla Firefox, or Microsoft Edge (latest versions)
- **Operating System:** Windows 10/11, macOS Ventura+, or Linux (Ubuntu 22.04+)
- **Required Files:** `app.py`, `utils.py`, `requirements.txt`, and sample data (`data/sample_telemetry.csv`)
- **Database:** SQLite (local `pump_data.db` auto-initialized on first run)
- **Environment Variables:** None required for local operation
- **Network Requirements:** Localhost connection (no external internet required after dependency installation)

## 3. Installation
Open your terminal and run the following commands:
```bash
git clone https://github.com/your-username/smartpump-analytics-dashboard.git
cd smartpump-analytics-dashboard
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

## 4. Quick Start
1. Ensure your virtual environment is active and dependencies are installed.
2. Start the application:
   ```bash
   streamlit run app.py
   ```
3. Open your web browser and navigate to **`http://localhost:8501`**.
4. Load the sample data (`data/sample_telemetry.csv`) using the sidebar file uploader.
5. Select the target pump ID and click **Run Analysis**.
6. Review the interactive efficiency curves and health status dashboard.

## 5. Normal Operation
1. **Upload Data:** In the sidebar, upload a valid CSV telemetry file or click "Load Sample Dataset".
2. **Select Parameters:** Choose the specific Pump ID and operating thresholds from the dropdown menus.
3. **Run Calculation:** Click the **Calculate Efficiency & Health** button.
4. **Interpret Results:** View the generated head-flow curve, overall efficiency percentage, and system health status badge.

## 6. Inputs and Units
- **Required Inputs:** 
  - `timestamp` (ISO 8601 format: YYYY-MM-DD HH:MM:SS)
  - `pump_id` (String / Alphanumeric)
  - `flow_rate` (Expected Unit: Cubic meters per hour, $m^3/h$)
  - `head_pressure` (Expected Unit: Meters of head, $m$)
  - `power_input` (Expected Unit: Kilowatts, $kW$)
- **Optional Inputs:** 
  - `fluid_temperature` (Expected Unit: Celsius, °C; default assumption: 20°C if missing)
- **Supported Ranges:** Flow rate (0 to 500 $m^3/h$), Head pressure (0 to 150 $m$), Power input (0 to 300 $kW$).
- **Accepted File Formats:** CSV (.csv) with header row matching exact column schema.

## 7. What the Tool Refuses
The application will intentionally halt execution and display an error banner when:
- Required columns (`flow_rate`, `head_pressure`, `power_input`) are missing from the uploaded CSV.
- Negative values are detected for flow rate, head pressure, or power.
- Input values exceed physical engineering limits (e.g., flow rate > 1000 $m^3/h$).
- The uploaded file format is not a valid CSV.

## 8. Expected Output
Successful execution generates:
- **Calculations:** Hydraulic power, shaft power, and pump efficiency percentage.
- **Tables:** Summary statistics table showing min, max, and mean operating parameters.
- **Charts:** Interactive Plotly Head-Flow performance curve with manufacturer benchmark overlay.
- **Status Messages:** Success banner indicating successful data ingestion and model calculation.

## 9. System Health and Alerts
The application displays one of four distinct health states:
- **HEALTHY:** Operating within normal parameters; efficiency > 75%.
- **DEGRADED:** Minor drop in efficiency (60%–75%) or elevated vibration/temperature trends; requires scheduled inspection.
- **FAILED:** Critical threshold breached (efficiency < 60% or severe cavitation detected); immediate shutdown required.
- **RECOVERING:** Post-maintenance telemetry stabilization phase; operating parameters re-establishing baseline.

## 10. Logs
- **Location:** Stored locally in `logs/app.log`.
- **Contents:** Timestamped event logs, data validation warnings, calculation exceptions, and startup/shutdown events.
- **How to view:** Open `logs/app.log` in any text editor or view the live stream in the developer tab of the app UI.
- **Diagnostic use:** Helps isolate whether an error stems from malformed input data, missing dependencies, or unhandled calculation exceptions.

## 11. Troubleshooting
| Problem | Possible Cause | What to Check |
| :--- | :--- | :--- |
| Application does not start | Missing dependencies / virtual environment not activated | Verify `requirements.txt` is installed and `.venv` is active |
| "Invalid CSV Structure" error | Incorrect column headers or missing required fields | Check column names against schema in Section 6 |
| Blank charts / No results displayed | Zero or null values in selected pump telemetry | Inspect CSV file for missing data rows or out-of-range values |

## 12. Recovery Procedures
**Procedure: Recovering from Corrupted Database / State**
1. Stop the Streamlit server (`Ctrl + C` in terminal).
2. Delete the local SQLite database file: `rm pump_data.db` (or delete via file explorer).
3. Restart the application: `streamlit run app.py`. The database will auto-reinitialize with default schema.
4. Re-upload your telemetry CSV file.

## 13. Assumptions
- All temperature values are assumed to be in Celsius (°C) unless explicitly specified otherwise.
- Water density is assumed constant at $1000 \text{ kg/m}^3$ for hydraulic power calculations.
- Timestamps in input files are synchronized to UTC.

## 14. Known Limitations
- The application does not independently verify physical sensor calibration or sensor drift.
- Supports single-phase and standard centrifugal pumps; does not currently model positive displacement pumps.
- Maximum file upload size is capped at 50 MB for local performance reasons.

## 15. Testing
Run the automated test suite using pytest:
```bash
pytest
```
Or run with verbose output:
```bash
python -m pytest -v
```

## 16. AI Usage
- **AI_LOG.md reference:** AI tools were used during development to draft initial Plotly visualization scripts and unit test templates. All AI-generated outputs were rigorously peer-reviewed, tested against edge cases, and modified to fit plant engineering standards.
