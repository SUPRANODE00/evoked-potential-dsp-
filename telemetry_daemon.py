import json
import re
import sqlite3
import subprocess
from datetime import datetime, timezone

DB_NAME = "telemetry_vault.db"


def init_db(db_path=DB_NAME):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS spatial_sweeps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            ta_origin REAL NOT NULL,
            peak_freq REAL NOT NULL,
            peak_power REAL NOT NULL,
            raw_payload TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def parse_octave_stream():
    cmd = ["octave", "--silent", "radius_sweep_engine.m"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Octave Execution Failed: {result.stderr}")

    ta_origin = 234.0
    peak_freq = 0.0
    peak_power = 0.0

    ta_match = re.search(r"TA Origin Baseline:\s*([\d\.]+)", result.stdout)
    if ta_match:
        ta_origin = float(ta_match.group(1))

    freq_match = re.search(
        r"Dominant Frequency Peak Detected:\s*([\d\.]+)\s*Hz\s*\(Magnitude:\s*([\d\.]+)\)",
        result.stdout,
    )
    if freq_match:
        peak_freq = float(freq_match.group(1))
        peak_power = float(freq_match.group(2))

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ta_origin": ta_origin,
        "peak_freq": peak_freq,
        "peak_power": peak_power,
        "stdout": result.stdout,
    }


def log_telemetry(payload, db_path=DB_NAME):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO spatial_sweeps (timestamp, ta_origin, peak_freq, peak_power, raw_payload)
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            payload["timestamp"],
            payload["ta_origin"],
            payload["peak_freq"],
            payload["peak_power"],
            json.dumps(payload),
        ),
    )
    conn.commit()
    conn.close()


def run():
    init_db()
    data = parse_octave_stream()
    log_telemetry(data)
    return data


if __name__ == "__main__":
    run()
