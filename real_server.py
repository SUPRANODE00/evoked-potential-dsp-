import http.server
import json
import os
import sqlite3
import tomllib
from datetime import datetime, timezone

import psutil

DB_PATH = "counter_grid_telemetry.db"
LOCK_FILE = "node_lock.json"
CONFIG_TOML = "compartment_union.toml"


def get_toml_config():
    if os.path.exists(CONFIG_TOML):
        with open(CONFIG_TOML, "rb") as f:
            return tomllib.load(f)
    return {}


class RealGridHandler(http.server.BaseHTTPRequestHandler):
    def _headers(self, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("X-Resource-Allocation", "ELECTRONEGATIVE_BLACKFLAME")
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/v1/grid/status":
            lock = {}
            if os.path.exists(LOCK_FILE):
                with open(LOCK_FILE, "r") as f:
                    lock = json.load(f)
            cfg = get_toml_config()

            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM threat_suppression_logs")
            total = cur.fetchone()[0]
            query = (
                "SELECT id, timestamp, center_freq_mhz, cancellation_metric, status "
                "FROM threat_suppression_logs ORDER BY id DESC LIMIT 1"
            )
            cur.execute(query)
            last_rec = cur.fetchone()
            conn.close()

            mem = psutil.virtual_memory()
            payload = {
                "node_id": lock.get("node_id", "SUPRANODE00_ORIGIN"),
                "domain": lock.get("domain", "erikivanrivera.blackcorp.me"),
                "contact": lock.get("contact", "erik.ivan.rivera@blackcorp.me"),
                "resource_allocation": "ELECTRONEGATIVE_BLACKFLAME",
                "compartment_encryption": cfg.get("encryption", {}),
                "url_scheme": cfg.get("url_scheme", {}),
                "real_hardware_metrics": {
                    "cpu_percent": psutil.cpu_percent(interval=None),
                    "ram_used_mb": round(mem.used / (1024 * 1024), 2),
                    "ram_total_mb": round(mem.total / (1024 * 1024), 2),
                    "host_pid": os.getpid(),
                },
                "coordinates": lock.get("spatial_coordinates", {}),
                "lock_status": lock.get("lock_status", "LOCKED"),
                "total_suppressed": total,
                "last_logged_entry": {
                    "id": last_rec[0] if last_rec else None,
                    "timestamp": last_rec[1] if last_rec else None,
                    "freq_mhz": last_rec[2] if last_rec else None,
                    "cancellation_metric": last_rec[3] if last_rec else None,
                    "status": last_rec[4] if last_rec else None,
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            self._headers(200)
            self.wfile.write(json.dumps(payload, indent=4).encode())

    def do_POST(self):
        if self.path == "/api/v1/grid/nullify":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode() if length else "{}")
            freq = float(body.get("freq_mhz", 2400.0))
            amp = float(body.get("amplitude", 1.0))
            ts = datetime.now(timezone.utc).isoformat()
            c_metric = -abs(amp * freq)

            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            query = (
                "INSERT INTO threat_suppression_logs "
                "(timestamp, center_freq_mhz, ingress_amplitude, "
                "phase_shift_deg, cancellation_metric, status) "
                "VALUES (?, ?, ?, 180.0, ?, 'NULLIFIED')"
            )
            cur.execute(query, (ts, freq, amp, c_metric))
            conn.commit()
            last_id = cur.lastrowid
            conn.close()

            payload = {
                "transaction_id": last_id,
                "timestamp": ts,
                "allocation_mode": "ELECTRONEGATIVE_BLACKFLAME",
                "center_freq_mhz": freq,
                "cancellation_metric": c_metric,
                "status": "NULLIFIED",
            }
            self._headers(200)
            self.wfile.write(json.dumps(payload, indent=4).encode())


if __name__ == "__main__":
    http.server.HTTPServer(("0.0.0.0", 3030), RealGridHandler).serve_forever()
