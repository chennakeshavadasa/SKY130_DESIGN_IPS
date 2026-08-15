import subprocess
import os
import numpy as np

# --- CONFIGURATION ---
NETLIST_FILE = "cmos_schmitt_trigger.spice"
TMP_FILE = "tmp_sweep.spice"

# Define the search grid to locate the 1.4V / 1.6V sweet spot
# Slicing NMOS widths below 1.0u gives the PMOS the power it needs
w1_values = [0.4, 0.5, 0.6, 0.8, 1.0]
w2_values = [1.0, 1.5, 2.0, 3.0, 4.0]
l_values  = [1.0, 1.5, 2.0, 2.5]

def run_simulation(w1, w2, length):
    # Read the original baseline netlist
    with open(NETLIST_FILE, 'r') as f:
        lines = f.readlines()

    # Inject the swept parameters into the netlist rows
    with open(TMP_FILE, 'w') as f:
        for line in lines:
            if "XM1 " in line:
                f.write(f"XM1 net1 VIN 0 GND sky130_fd_pr__nfet_01v8 L={length} W={w1} nf=1 mult=1\n")
            elif "XM2 " in line:
                f.write(f"XM2 VOUT VIN net1 GND sky130_fd_pr__nfet_01v8 L={length} W={w2} nf=1 mult=1\n")
            # Force ngspice to print out the exact trip timestamps to stdout
            elif ".control" in line:
                f.write(line)
                f.write("run\n")
                # Look for the exact time when Vout crosses VDD/2 (0.9V)
                f.write("meas tran t_fall when v(VOUT)=0.9 fall=1\n")
                f.write("meas tran t_rise when v(VOUT)=0.9 rise=1\n")
            else:
                f.write(line)

    # Invoke ngspice in batch mode
    proc = subprocess.Popen(
        ["ngspice", "-b", TMP_FILE],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, _ = proc.communicate()

    # Parse out the measurement time variables
    t_fall, t_rise = None, None
    for line in stdout.split('\n'):
        if "t_fall" in line and "=" in line:
            t_fall = float(line.split('=')[1].split()[0])
        if "t_rise" in line and "=" in line:
            t_rise = float(line.split('=')[1].split()[0])

    # Clean up the loop netlist file
    if os.path.exists(TMP_FILE):
        os.remove(TMP_FILE)

    return t_fall, t_rise

# --- MAIN SWEEP ENGINE ---
print(f"{'W1':<6} {'W2':<6} {'L':<6} | {'V_PH (Goal: 1.6V)':<18} | {'V_PL (Goal: 1.4V)':<18}")
print("-" * 65)

best_match = None
min_error = float('inf')

for l in l_values:
    for w1 in w1_values:
        for w2 in w2_values:
            t_f, t_r = run_simulation(w1, w2, l)

            if t_f is not None and t_r is not None:
                # Convert transient timeline timestamps back into voltages
                # Input ramps up 0V -> 1.8V in 1ms, then down 1.8V -> 0V in 1ms
                v_ph = t_f * 1800.0
                v_pl = 1.8 - ((t_r - 0.001) * 1800.0)

                print(f"{w1:<6} {w2:<6} {l:<6} | {v_ph:<18.3f} | {v_pl:<18.3f}")

                # Check how close we are to targets
                error = abs(v_ph - 1.6) + abs(v_pl - 1.4)
                if error < min_error:
                    min_error = error
                    best_match = (w1, w2, l, v_ph, v_pl)

print("=" * 65)
if best_match:
    print(f"Optimal Convergence Sizing Found!")
    print(f"XM1 Width: {best_match[0]}u")
    print(f"XM2 Width: {best_match[1]}u")
    print(f"Both Lengths: {best_match[2]}u")
    print(f"Yielding thresholds: V_PH = {best_match[3]:.3f}V, V_PL = {best_match[4]:.3f}V")
