import csv
import os
import time


def read_resonance(path):
    #script will get the most recent resonance from a given transitions resonance log csv
    with open(path, mode="r", newline="", encoding="utf-8-sig") as f:
        sample = f.read(2048)
        f.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters=",")

        rows = list(csv.DictReader(f, dialect=dialect)) #get all rows
        if not rows:
            raise ValueError("CSV has no data rows")

        row = rows[-1]  # last row
        row = {(k or "").strip(): (v or "").strip() for k, v in row.items()}

        return  float(row["Resonant Detuning"])

def write_most_recent_resonance(path, resonance):
    #script will write the most recent resonance to a given transitions resonance log csv
    fieldnames = ["DateTime", "Resonant Detuning"]
    file_exists = os.path.isfile(path)
    with open(path, mode="a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({"DateTime": time.strftime("%Y-%m-%d %H:%M:%S"), "Resonant Detuning": resonance})
