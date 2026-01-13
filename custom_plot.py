
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from obspy import UTCDateTime, Inventory, read, read_inventory
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
# Default: None (Auto-scaled by the plotting function)
MY_MIN_BRIGHTNESS = None
MY_MAX_BRIGHTNESS = None
MY_START_TIME     = None
MY_END_TIME       = None

# ==========================================
# 2. SCRIPT EXECUTION
# ==========================================

def run_custom_plot():
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

    # Check if input path exists
    if not os.path.exists(ssa_results_path):
        print(f"[ERROR] The SSA results directory does not exist: '{ssa_results_path}'")
        print("Please check 'ssa_results_path' in 'plot_config.yaml'.")
        return

    # Critical File Check
    critical_file = os.path.join(ssa_results_path, "out_Max.npy")
    if not os.path.exists(critical_file):
        print(f"[ERROR] Could not find 'out_Max.npy' in: {ssa_results_path}")
        print("This file is required for plotting. Did SSA2py finish successfully?")
        return

    print("Generating custom plot...")
    print(f"Params: MinBright={MY_MIN_BRIGHTNESS}, MaxBright={MY_MAX_BRIGHTNESS}, Range={MY_START_TIME}-{MY_END_TIME}s")

    # ==========================================
    # DATA LOADING (Mimicking SSA2py codebase)
    # ==========================================
    
    # 1. Infer Event Directory and Data Names from 'ssa_results_path'
    # Structure: .../Events/TIME/Results/SSA/MSEED_NAME/Detailed_Solution
    try:
        # detailed_sol_dir = .../Detailed_Solution
        mseed_base_name = os.path.basename(os.path.dirname(ssa_results_path)) # e.g. ENV_2.0_8.0_E
        results_ssa_dir = os.path.dirname(os.path.dirname(ssa_results_path))   # .../Results/SSA
        results_dir = os.path.dirname(results_ssa_dir)                         # .../Results
        event_dir = os.path.dirname(results_dir)                               # .../Events/TIME
        
        print(f"[INFO] Inferred Event Directory: {event_dir}")
        print(f"[INFO] Inferred Data Base Name: {mseed_base_name}")

        # 2. Load Inventory
        inventory_path = os.path.join(event_dir, "Inventory", "inventory.xml")
        if os.path.exists(inventory_path):
            print(f"[INFO] Loading Inventory from: {inventory_path}")
            inv_obj = read_inventory(inventory_path)
            # Mimic config.inv
            config.inv = inv_obj 
        else:
            print(f"[WARNING] Inventory file not found at {inventory_path}. Plot will miss station icons.")
            inv_obj = Inventory()

        # 3. Load Waveforms (to get stations_used)
        # The mseed file should be in Processed_Data/{mseed_base_name}.mseed
        mseed_path = os.path.join(event_dir, "Processed_Data", f"{mseed_base_name}.mseed")
        
        stations_used_list = []
        if os.path.exists(mseed_path):
             print(f"[INFO] Loading Waveforms from: {mseed_path}")
             st = read(mseed_path)
             # Mimic creation of stations_used list from plot_res.py
             # stations_used = [tr.stats.network+'.'+tr.stats.station for tr in config.st]
             stations_used_list = list(set([tr.stats.network + '.' + tr.stats.station for tr in st]))
             print(f"[INFO] Found {len(stations_used_list)} stations used.")
             # Update global config.st as plot_res_ expects it sometimes
             config.st = st
        else:
             print(f"[WARNING] Processed mseed file not found at {mseed_path}. Stations will not be plotted.")

    except Exception as e:
        print(f"[ERROR] Failed to load associated data (Inventory/Waveforms): {e}")
        inv_obj = Inventory()
        stations_used_list = []

    try:
        MaxBrightTimeStep_(
            brpath=ssa_results_path,
            brpathboot=[], # No bootstrap
            evla=event_lat,
            evlo=event_lon,
            evdepth=event_depth,
            time=origin_time,
            inv=inv_obj, # Pass the loaded inventory
            stations_used=stations_used_list, # Pass the real stations list
            
            # CUSTOM VALUES
            startTime=MY_START_TIME,
            endTime=MY_END_TIME,
            minBrig=MY_MIN_BRIGHTNESS,
            maxBrig=MY_MAX_BRIGHTNESS,
            
            # Standard settings
            points_size=8,        # Original: 8
            maxgrid=100,
            faults=False, 
            grid=True,
            hypo=True,
            colormap='rainbow',   # Original: 'rainbow'
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
