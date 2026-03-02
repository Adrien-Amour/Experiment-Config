import time
from adriq.ad9910 import (
    general_setting_standalone,
    single_tone_profile_setting,
    interpolate_rf_power
)

# Config for 866 RP from dds_config.cfg
PORT = "COM9"
BOARD = 3
CALIBRATION_FILE = r"C:\Users\probe\OneDrive - University of Sussex\Desktop\Experiment_Config\AOM_Calibrations\866rp_calib.csv"
CENTRAL_FREQUENCY = 400.0  # MHz (centre_f)
N_PASSES = 2               # n_passes

# Test parameters
detunings = [0.0, 5.0, -5.0]          # MHz
fractions = [0.02, 0.05, 0.1, 0.2, 0.3]  # fractional optical power (0–1)

def calc_dds_freq(detuning):
    return (detuning + CENTRAL_FREQUENCY) / N_PASSES  # internal DDS frequency

def main():
    print("Applying general standalone settings...")

    results = []
    try:
        for d in detunings:
            f_dds = calc_dds_freq(d)
            print(f"\nDetuning={d} MHz -> DDS freq={f_dds:.3f} MHz")
            for frac in fractions:
                amplitude, optical_power = interpolate_rf_power(CALIBRATION_FILE, frac, f_dds)
                print(f"  frac={frac:.3f} -> amplitude={amplitude}, optical_power≈{optical_power*1e3:.3f} mW")
                # Send profile (Phase_Offset=0)
                single_tone_profile_setting(
                    Port=PORT,
                    Board=BOARD,
                    Profile=3,
                    Amplitude=amplitude,
                    Phase_Offset=0,
                    Frequency=f_dds,
                    Verbose=False
                )
                time.sleep(5)
                results.append((d, f_dds, frac, amplitude, optical_power))
    finally:
        # Safety: turn off amplitude
        single_tone_profile_setting(
            Port=PORT,
            Board=BOARD,
            Profile=3,
            Amplitude=0,
            Phase_Offset=0,
            Frequency=calc_dds_freq(0.0),
            Verbose=False
        )
        print("\nReset amplitude to 0.")

    # Optional: simple summary
    print("\nSummary:")
    for r in results:
        d, f_dds, frac, amp, opt = r
        print(f"Detuning {d:+.1f} MHz | DDS {f_dds:.2f} MHz | frac {frac:.3f} | amp {amp} | opt {opt*1e3:.3f} mW")

if __name__ == "__main__":
    main()