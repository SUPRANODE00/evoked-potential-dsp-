import sqlite3


class ReceptiveSensorBridge:
    def __init__(self, origin_lat=29.7604, origin_lon=-95.3698, origin_alt=150.0):
        # Realigned Origin Baseline (Houston Matrix Center)
        self.origin = {"lat": origin_lat, "lon": origin_lon, "alt": origin_alt}
        self.compass_heading = 0.0  # Normalized 0-360 true north
        self.camera_pitch = 0.0  # Optical orientation

    def realign_compass_and_camera(self, heading=0.0, pitch=0.0):
        """Banish stale loops and lock orientation to true grid origin."""
        self.compass_heading = heading % 360.0
        self.camera_pitch = max(-90.0, min(90.0, pitch))
        print(
            f"[+] Realigned Origin -> Compass: {self.compass_heading:.1f}° | Camera Pitch: {self.camera_pitch:.1f}°"
        )

    def format_section_508_accessible_feedback(self, rf_freq, signal_strength_dbm):
        """
        Section 508 / Assistive Technology Interface:
        Translates raw RF oscillation metrics into high-contrast visual status indicators
        and visual-tactile pulse frequencies for hard of hearing / deaf operators.
        """
        # Map signal strength to optical strobe frequency (Hz)
        visual_strobe_hz = max(1, int((signal_strength_dbm + 100) / 10))

        # Section 508 Compliant Status Patterns
        if signal_strength_dbm > -65:
            accessibility_label = "SIGNAL_OPTIMAL [HIGH-CONTRAST FLASH: FAST PULSE]"
            haptic_pattern = "••• (3 Short Pulses)"
        elif signal_strength_dbm > -85:
            accessibility_label = "SIGNAL_STABLE [HIGH-CONTRAST FLASH: MEDIUM PULSE]"
            haptic_pattern = "•• (2 Medium Pulses)"
        else:
            accessibility_label = (
                "SIGNAL_WEAK [HIGH-CONTRAST FLASH: LONG WARNING PULSE]"
            )
            haptic_pattern = "— (1 Long Pulse)"

        return {
            "frequency_mhz": rf_freq,
            "signal_dbm": signal_strength_dbm,
            "strobe_rate_hz": visual_strobe_hz,
            "visual_indicator": accessibility_label,
            "haptic_feedback": haptic_pattern,
        }


def execute_receptive_sync():
    bridge = ReceptiveSensorBridge()
    bridge.realign_compass_and_camera(heading=0.0, pitch=0.0)

    conn = sqlite3.connect("node_telemetry.db")
    cursor = conn.cursor()

    # Table for 508-accessible signal logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accessible_sensor_logs (
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            compass_heading REAL,
            camera_pitch REAL,
            rf_freq_mhz REAL,
            strobe_rate_hz INTEGER,
            visual_status TEXT,
            haptic_pattern TEXT
        )
    """)

    # Sample optic-receptive sensor sweep
    test_signals = [(915.0, -55), (908.0, -72), (927.0, -90)]
    for freq, dbm in test_signals:
        feedback = bridge.format_section_508_accessible_feedback(freq, dbm)
        cursor.execute(
            """
            INSERT INTO accessible_sensor_logs 
            (compass_heading, camera_pitch, rf_freq_mhz, strobe_rate_hz, visual_status, haptic_pattern)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                bridge.compass_heading,
                bridge.camera_pitch,
                freq,
                feedback["strobe_rate_hz"],
                feedback["visual_indicator"],
                feedback["haptic_feedback"],
            ),
        )

        print(
            f"[508 ACCESS] {feedback['visual_indicator']} | Haptic: {feedback['haptic_feedback']} | Strobe: {feedback['strobe_rate_hz']}Hz"
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    execute_receptive_sync()
