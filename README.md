# Custom SSA2py Plotter

This script allows you to re-plot **SSA2py** results with custom brightness thresholds (`minBrig`, `maxBrig`) and time ranges (`startTime`, `endTime`) without re-running the computationally expensive Backprojection / Source Scanning Algorithm.

## Prerequisites

1.  **SSA2py Installed**: This script imports functions from `SSA2py`. It must be run in an environment where `SSA2py` is installed or accessible in your `PYTHONPATH`.
2.  **Existing Results**: You must have already run `SSA2py.py` for an event and generated results (specifically the `out_Max.npy` files).

## Setup

1.  Place `custom_plot.py` in your `SSA2py` project directory (or any directory where it can import `SSA2py`).
2.  Open `custom_plot.py` in a text editor.

## Configuration

Edit the **Section 1: SETUP YOUR CUSTOM PARAMETERS HERE** at the top of the file:

### 1. Set the Data Path
Point `ssa_results_path` to the specific output folder of your event containing the `.npy` files.
```python
ssa_results_path = "/full/path/to/SSA2py/Events/[EVENT_DATE]/Results/SSA/[PROCESSED_DATA_NAME]/Detailed_Solution"
```

### 2. Set Event Details
Fill in the event metadata (used for plotting the star and calculated distances).
```python
event_lat = 37.24
event_lon = 20.49
event_depth = 10.0
origin_time = UTCDateTime("2023-01-01T12:00:00")
```

### 3. Set Custom Plotting Values
Adjust the limits as needed. Set to `None` to use defaults (auto-scaling).
```python
MY_MIN_BRIGHTNESS = 0.6   # Minimum brightness threshold
MY_MAX_BRIGHTNESS = 1.0   # Maximum brightness threshold
MY_START_TIME     = 10    # Start plotting 10s after origin
MY_END_TIME       = 50    # Stop plotting 50s after origin
```

## Usage

Run the script with Python 3:

```bash
python3 custom_plot.py
```

The new plot will be saved in the `./Custom_Plots` folder as `Custom_MaximumBrightness.png`.
