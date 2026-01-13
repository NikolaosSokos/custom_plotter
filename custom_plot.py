
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

# ==========================================
# 1. SETUP
# ==========================================

# Read paths from plot_config.yaml
# We reuse the config.read function from SSA2py to parse the YAML
try:
    if os.path.exists("plot_config.yaml"):
        _p_cfg = config.read("plot_config.yaml")
        ssa_results_path = _p_cfg.get('ssa_results_path')
        output_path = _p_cfg.get('output_path', './Custom_Plots')
    elif os.path.exists("custom_ssa_plotter/plot_config.yaml"):
         # specific check if running from root but config is in subfolder
        _p_cfg = config.read("custom_ssa_plotter/plot_config.yaml")
        ssa_results_path = _p_cfg.get('ssa_results_path')
        output_path = _p_cfg.get('output_path', './Custom_Plots')
    else:
        # Fallback provided for safety, or error out
        print("Error: plot_config.yaml not found.")
        sys.exit(1)
except Exception as e:
    print(f"Error reading plot_config.yaml: {e}")
    sys.exit(1)

# Event Details (Update these to match your event)
# These remain in the script as requested (config only for paths)
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

    # Load the actual configuration from the file
    # This allows us to use the attributes defined in the codebase logic
    if os.path.exists("./config.yaml"):
        config.cfg = config.read("./config.yaml")
    else:
        print("Warning: ./config.yaml not found, using minimal defaults")
        config.cfg = {'Plotting': {'Topography/Bathymetry': [False, ''], 'Save Layers': './SSA2py/figure_layers'}, 'Backprojection': {'Grid': [[0.0, 9.0, ['box', 50, 50, 0, 20, 1]]]}}

    # Initialize Logger (Required by SSA2py functions)
    class DummyLogger:
        def warning(self, msg): print(f"[WARNING] {msg}")
        def info(self, msg): print(f"[INFO] {msg}")
        def error(self, msg): print(f"[ERROR] {msg}")
    config.logger = DummyLogger()
    
    # Calculate gridRules using the library's own logic
    # This avoids "extra attributes" by deriving them from the config as the main app does
    # We check for a generic high magnitude coverage (e.g., 5.0) to get a valid grid rule
    try:
        config.gridRules = config.rules(5.0, config.cfg['Backprojection']['Grid'])
    except Exception:
        # Fallback if config interpretation fails
        config.gridRules = [['box']]

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
