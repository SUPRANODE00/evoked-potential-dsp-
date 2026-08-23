import runpy
import sqlite3
from unittest.mock import MagicMock, patch

import pytest

import telemetry_daemon


@pytest.fixture
def temp_db(tmp_path):
    db_file = str(tmp_path / "test_vault.db")
    telemetry_daemon.init_db(db_file)
    return db_file


def test_init_db(temp_db):
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='spatial_sweeps'"
    )
    table = cursor.fetchone()
    conn.close()
    assert table is not None


def test_log_telemetry(temp_db):
    payload = {
        "timestamp": "2026-08-23T12:00:00Z",
        "ta_origin": 234.0,
        "peak_freq": 59.57,
        "peak_power": 0.45,
        "stdout": "test output",
    }
    telemetry_daemon.log_telemetry(payload, db_path=temp_db)

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT ta_origin, peak_freq, peak_power FROM spatial_sweeps")
    row = cursor.fetchone()
    conn.close()

    assert row[0] == 234.0
    assert row[1] == 59.57
    assert row[2] == 0.45


@patch("subprocess.run")
def test_parse_octave_stream_success(mock_run):
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout="[+] TA Origin Baseline: 234.0 meters\n[+] Dominant Frequency Peak Detected: 59.57 Hz (Magnitude: 0.4568)\n",
    )
    data = telemetry_daemon.parse_octave_stream()
    assert data["ta_origin"] == 234.0
    assert data["peak_freq"] == 59.57
    assert data["peak_power"] == 0.4568


@patch("subprocess.run")
def test_parse_octave_stream_failure(mock_run):
    mock_run.return_value = MagicMock(returncode=1, stderr="Octave error")
    with pytest.raises(RuntimeError):
        telemetry_daemon.parse_octave_stream()


@patch("telemetry_daemon.log_telemetry")
@patch("telemetry_daemon.parse_octave_stream")
@patch("telemetry_daemon.init_db")
def test_run(mock_init, mock_parse, mock_log):
    mock_parse.return_value = {"status": "ok"}
    res = telemetry_daemon.run()
    assert res == {"status": "ok"}
    mock_init.assert_called_once()
    mock_log.assert_called_once()


@patch("subprocess.run")
def test_main_block(mock_run):
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout="[+] TA Origin Baseline: 234.0 meters\n[+] Dominant Frequency Peak Detected: 59.57 Hz (Magnitude: 0.4568)\n",
    )
    runpy.run_module("telemetry_daemon", run_name="__main__")
    mock_run.assert_called_once()
