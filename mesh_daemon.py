import math
import random
import sqlite3
import time


def calculate_volume_block(x, y, z, ir_dist):
    # Computes 3D spherical prism volume centered at node origin (xyz)
    radius = max(ir_dist / 100.0, 1.0)
    volume_block = (4 / 3) * math.pi * (radius**3)
    return volume_block


def run_telemetry_cycle():
    conn = sqlite3.connect("node_telemetry.db")
    cursor = conn.cursor()

    # Base telemetry parameters
    node_id = "UAV-MESH-ORIGIN-01"
    x, y, z = 29.7604, -95.3698, 150.0
    channels = [902.5, 908.0, 915.0, 921.5, 927.0]

    print(f"[*] Starting Active Sensor & Telecom Mesh Daemon for Node: {node_id}")

    for cycle in range(1, 6):
        # 1. Frequency Hopping
        current_freq = random.choice(channels)
        ir_metric = 1250.0 + random.uniform(-10.0, 10.0)

        # 2. Inverted Volume Calculation
        vol_block = calculate_volume_block(x, y, z, ir_metric)
        neg_volume_block = -vol_block  # -(topic.subject.block.volume)

        # 3. Log Active Telemetry Payload
        cursor.execute(
            """
            INSERT INTO mesh_telemetry (node_id, x_coord, y_coord, z_coord, rf_freq_mhz, ir_distance_m, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (node_id, x, y, z, current_freq, ir_metric, "ACTIVE_ENCRYPTED"),
        )

        # 4. Inverted Mirroring & Disaster Recovery Logging
        cursor.execute(
            """
            INSERT INTO disaster_recovery_state (node_id, neg_volume_block, zero_signal_ground, restoration_status)
            VALUES (?, ?, ?, ?)
        """,
            (node_id, neg_volume_block, "SYNCED_FE80::2", "STANDBY_MIRROR"),
        )

        conn.commit()
        print(
            f"[CYCLE {cycle}] RF: {current_freq} MHz | IR Metric: {ir_metric:.2f}m | Inverted Vol: {neg_volume_block:.2f} | Status: NOMINAL"
        )
        time.sleep(1)

    conn.close()


if __name__ == "__main__":
    run_telemetry_cycle()
