import csv
import os
import sys
import numpy as np

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

def load_calibration(path):
    with open(path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        raise ValueError("File empty.")
    header = rows[0]
    try:
        max_rf_power = float(header[0])
        fracs = [float(x) for x in header[1:]]
    except Exception as e:
        raise ValueError(f"Header parse error: {e}")
    freq = []
    powers = []
    for r in rows[1:]:
        if len(r) != len(header):
            raise ValueError("Row length mismatch.")
        freq.append(float(r[0]))
        powers.append([float(x) for x in r[1:]])
    return max_rf_power, np.array(fracs), np.array(freq), np.array(powers)

def subtract_background(powers, bg):
    out = powers - bg
    out[out < 0] = 0.0
    return out

def edit_calibration(max_rf_power, fracs, freq, powers, N):
    if N < 1 or N > len(fracs):
        raise ValueError("N out of range.")
    # Remove first N fractional columns
    kept_fracs = fracs[N:]  # fractions after discarding
    kept_powers = powers[:, N:]
    # Insert zero-power synthetic column
    zero_col = np.zeros((kept_powers.shape[0], 1))
    new_powers = np.concatenate([zero_col, kept_powers], axis=1)
    new_fracs = np.concatenate([[0.0], kept_fracs])
    return new_fracs, new_powers

def save_calibration(path, max_rf_power, fracs, freq, powers):
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        header = [f"{max_rf_power}"] + [f"{x}" for x in fracs]
        w.writerow(header)
        for f_mhz, row in zip(freq, powers):
            w.writerow([f_mhz] + [f"{val}" for val in row])
    print(f"Saved edited calibration to {path}")

def main():
    in_file = input("Input calibration CSV path: ").strip()
    if not os.path.isfile(in_file):
        print("File not found.")
        return
    out_file = input("Output (edited) CSV path: ").strip()
    bg_str = input("Background to subtract (numeric): ").strip()
    try:
        bg = float(bg_str)
    except:
        print("Invalid background.")
        return
    N_str = input("Number of initial low-power columns to discard (N): ").strip()
    if not N_str.isdigit():
        print("N must be integer.")
        return
    N = int(N_str)

    max_rf_power, fracs, freq, powers = load_calibration(in_file)
    print(f"Loaded: max_rf_power={max_rf_power}, columns={len(fracs)}, frequencies={len(freq)}")
    powers_bg = subtract_background(powers, bg)
    new_fracs, new_powers = edit_calibration(max_rf_power, fracs, freq, powers_bg, N)
    save_calibration(out_file, max_rf_power, new_fracs, freq, new_powers)

    # Optional quick visualization
    if plt:
        show = input("Plot before/after for one frequency? (y/n): ").strip().lower() == 'y'
        if show:
            # Pick middle frequency
            idx = len(freq)//2
            plt.figure(figsize=(6,4))
            plt.plot(fracs, powers[idx], 'o-', label='Original')
            plt.plot(fracs, powers_bg[idx], 'o--', label='Background subtracted')
            plt.plot(new_fracs, new_powers[idx], 's-', label='Edited (zero + truncated)')
            plt.xlabel("RF Fraction (original)")
            plt.ylabel("Optical Power")
            plt.title(f"Freq {freq[idx]} MHz")
            plt.legend()
            plt.tight_layout()
            plt.show()
    else:
        print("matplotlib not installed; skipping plot.")

if __name__ == "__main__":
    main()