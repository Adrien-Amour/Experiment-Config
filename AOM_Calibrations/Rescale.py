import csv

def rescale_calibration_data(input_file: str, output_file: str, scaling_factor: float):
    """Rescales optical power values in the calibration data by a given scaling factor.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file.
        scaling_factor (float): Factor to rescale the optical power values.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Iterate through rows of the file
        for row_index, row in enumerate(reader):
            rescaled_row = []
            for col_index, value in enumerate(row):
                try:
                    # Rescale only if not in the first row or first column
                    if row_index != 0 and col_index != 0:
                        rescaled_value = f"{float(value) * scaling_factor:.2E}"
                    else:
                        rescaled_value = value
                    rescaled_row.append(rescaled_value)
                except ValueError:
                    # Keep non-numeric values (like headers) as is
                    rescaled_row.append(value)
            writer.writerow(rescaled_row)

    print(f"Rescaled data has been saved to '{output_file}'.")

# Example usage
input_file_path = "866OP_calib_before_rescale.csv"  # Provide the correct path
output_file_path = "866OP_calib.csv"
scaling_factor = (1.74 / 1.89) * 1.74 / 5.48  # Example scaling factor

rescale_calibration_data(input_file_path, output_file_path, scaling_factor)