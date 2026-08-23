import os
import signal
import sqlite3
import subprocess


def cancel_grid_and_purge_streams():
    print("[!] INITIATING SYSTEM PURGE AND GRID CANCELLATION...")

    # 1. Terminate active background daemon processes
    try:
        pids = (
            subprocess.check_output(
                ["pgrep", "-f", "mesh_daemon.py|accessible_telemetry.py"]
            )
            .decode()
            .split()
        )
        for pid in pids:
            if int(pid) != os.getpid():
                os.kill(int(pid), signal.SIGTERM)
                print(f"[+] Banished background process PID: {pid}")
    except subprocess.CalledProcessError:
        print("[+] No active lab stream / daemon processes found in memory.")

    # 2. Clear SQLite databases and persistent state tables
    db_file = "node_telemetry.db"
    if os.path.exists(db_file):
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS mesh_telemetry")
            cursor.execute("DROP TABLE IF EXISTS disaster_recovery_state")
            cursor.execute("DROP TABLE IF EXISTS accessible_sensor_logs")
            conn.commit()
            conn.close()
            os.remove(db_file)
            print("[+] Cleared and purged local database tables and persistent logs.")
        except Exception as e:
            print(f"[-] Error purging database: {e}")

    # 3. Overwrite environment configuration to offline baseline
    with open("config.env", "w") as f:
        f.write("# GRID STATE: CANCELED / OFFLINE\n")
        f.write('NODE_STATE="OFFLINE_GROUNDED"\n')
        f.write("RF_CENTER_FREQ_MHZ=0.0\n")
        f.write('MIRROR_TUNNEL_STATE="DISABLED"\n')

    print(
        "[✓] Grid state canceled. All oscillating loops banished. System restored to baseline zero."
    )


if __name__ == "__main__":
    cancel_grid_and_purge_streams()
