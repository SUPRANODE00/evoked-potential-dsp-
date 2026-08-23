import sqlite3


def setup_telemetry_db():
    conn = sqlite3.connect("node_telemetry.db")
    cursor = conn.cursor()

    # Active Mesh Node Telemetry Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mesh_telemetry (
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            node_id TEXT,
            x_coord REAL,
            y_coord REAL,
            z_coord REAL,
            rf_freq_mhz REAL,
            ir_distance_m REAL,
            status TEXT
        )
    """)

    # Inverted Twin-Bot Disaster Recovery State Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disaster_recovery_state (
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            node_id TEXT,
            neg_volume_block REAL,
            zero_signal_ground TEXT,
            restoration_status TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("[+] Telemetry and Disaster Recovery Database Initialized.")


if __name__ == "__main__":
    setup_telemetry_db()
