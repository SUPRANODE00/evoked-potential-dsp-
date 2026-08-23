import sqlite3


def audit_database():
    conn = sqlite3.connect("node_telemetry.db")
    cursor = conn.cursor()

    print("=== ACTIVE MESH TELEMETRY LOGS ===")
    cursor.execute(
        "SELECT timestamp, node_id, rf_freq_mhz, ir_distance_m, status FROM mesh_telemetry"
    )
    for row in cursor.fetchall():
        print(
            f"Time: {row[0]} | Node: {row[1]} | Freq: {row[2]} MHz | IR Dist: {row[3]:.2f}m | Status: {row[4]}"
        )

    print("\n=== DISASTER RECOVERY INVERTED MATRIX LOGS ===")
    cursor.execute(
        "SELECT timestamp, node_id, neg_volume_block, zero_signal_ground, restoration_status FROM disaster_recovery_state"
    )
    for row in cursor.fetchall():
        print(
            f"Time: {row[0]} | Node: {row[1]} | NegVol: {row[2]:.2f} | Ground: {row[3]} | State: {row[4]}"
        )

    conn.close()


if __name__ == "__main__":
    audit_database()
