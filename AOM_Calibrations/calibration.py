from adriq.Thorlabs_Power_Meter import *


# List available COM ports
ports = list(serial.tools.list_ports.comports())
print("\nAvailable COM Ports:")
for port in ports:
    print(f"{port.device}: {port.description}")

# Prompt user for COM port, board number, and filename
port = input("\nEnter the COM port to use (e.g., COM9): ").strip()
board = int(input("Enter the DDS board number: ").strip())
calibration_file = input("Enter the filename to save the calibration results: ").strip()
default_profile_input = input("Enter the default DDS profile (0-7): ").strip()
if not default_profile_input.isdigit():
    raise ValueError("Profile must be an integer 0-7.")
profile = int(default_profile_input)
if not (0 <= profile <= 7):
    raise ValueError("Profile must be between 0 and 7.")


# Prompt for number of AOM passes (e.g., 1 for single-pass, 2 for double-pass)
num_passes_input = input("Enter the number of AOM passes (default 2): ").strip()
num_passes = int(num_passes_input) if num_passes_input else 2
if num_passes <= 0:
    raise ValueError("Number of passes must be a positive integer.")

rm = pyvisa.ResourceManager()
# Select a device from the list
resource_name = select_device(rm)
print(f"Selected device: {resource_name}")
pm100d = rm.open_resource(resource_name)
power_meter = ThorlabsPM100(pm100d)
# print(f"Connected to Power Meter: {power_meter.get_idn()}")
# Define the parameters
frequency_range = np.arange(360, 440.1, 2)

#frequency_range = np.array([400-18])

max_rf_power = int(input("\nEnter the max RF power the AOM can take: ").strip())

# Run the calibration
calibrate_dds(port, board, profile, calibration_file, frequency_range, max_rf_power, power_meter, num_rf_points=75, n_passes=num_passes)