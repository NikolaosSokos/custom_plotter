
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from obspy import UTCDateTime, Inventory
from SSA2py.core import config
# Import the plotting function from your local SSA2py installation
# Ensure this script is run from a location where SSA2py is importable
from SSA2py.core.plotting_functions.MaxBrightTimeStep import MaxBrightTimeStep_

# ==========================================
# 1. SETUP YOUR CUSTOM PARAMETERS HERE
# ==========================================

# Path to the directory containing your SSA results (where out_Max.npy is located)
# Example: "/path/to/SSA2py/Events/2023-01-01T12:00:00/Results/SSA/Processed_Data_.../Detailed_Solution"
ssa_results_path = "/Users/nsokos/Nikos/SSA2py/Events/2023-01-01T12:00:00/Results/SSA/Detailed_Solution"  # <--- UPDATE THIS

# Output directory for the new plot
output_path = "./Custom_Plots"

# Event Details (Update these to match your event)
event_lat = 37.24   
event_lon = 20.49   
event_depth = 10.0  
origin_time = UTCDateTime("2023-01-01T12:00:00") 

# Custom Brightness & Time Settings
MY_MIN_BRIGHTNESS = 0.5   # Set your custom minimum brightness (e.g., 0.5) or None
MY_MAX_BRIGHTNESS = 1.0   # Set your custom maximum brightness (e.g., 1.0) or None
MY_START_TIME     = 0     # Start time relative to origin (seconds) or None
MY_END_TIME       = 60    # End time relative to origin (seconds) or None

# ==========================================
# 2. SCRIPT EXECUTION
# ==========================================

def run_custom_plot():
    # Mocking the configuration needed by the function
    config.cfg = {
        'Plotting': {
            'Topography/Bathymetry': [False, ''],
            'Save Layers': './Layers' # Points to where SSA2py expects layers; adjust if needed
        },
        'gridRules': [['box']] 
    }

    # Dummy logger to suppress SSA2py logging noise
    class DummyLogger:
        def warning(self, msg): print(f"[WARNING] {msg}")
        def info(self, msg): print(f"[INFO] {msg}")
        def error(self, msg): print(f"[ERROR] {msg}")
    
    config.logger = DummyLogger()

    # Ensure output directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Check if input path exists
    if not os.path.exists(ssa_results_path):
        print(f"Error: The path '{ssa_results_path}' does not exist.")
        print("Please update 'ssa_results_path' in the script to point to your SSA results.")
        return

    print("Generating custom plot...")
    print(f"Params: MinBright={MY_MIN_BRIGHTNESS}, MaxBright={MY_MAX_BRIGHTNESS}, Range={MY_START_TIME}-{MY_END_TIME}s")

    try:
        MaxBrightTimeStep_(
            brpath=ssa_results_path,
            brpathboot=[], # No bootstrap
            evla=event_lat,
            evlo=event_lon,
            evdepth=event_depth,
            time=origin_time,
            inv=Inventory(), # Empty inventory (no stations plotted)
            stations_used=[], # Empty list
            
            # CUSTOM VALUES
            startTime=MY_START_TIME,
            endTime=MY_END_TIME,
            minBrig=MY_MIN_BRIGHTNESS,
            maxBrig=MY_MAX_BRIGHTNESS,
            
            # Standard settings
            points_size=10,
            maxgrid=100,
            faults=False, 
            grid=True,
            hypo=True,
            colormap='plasma',
            topo=False,   
            meridian=True,
            info_box=True,
            Test='MAIN',
            autoselect=False, # Essential for manual limits
            filename='Custom_MaximumBrightness',
            outpath=output_path,
            fileformat='png',
            dpi=300
        )
        print(f"Success! Plot saved to: {os.path.abspath(output_path)}/Custom_MaximumBrightness.png")
        
    except Exception as e:
        print(f"An error occurred during plotting: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_custom_plot()
