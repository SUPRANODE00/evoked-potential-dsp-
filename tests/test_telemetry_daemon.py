import runpy
from unittest.mock import MagicMock, patch

import pytest

import telemetry_daemon


@patch("subprocess.run")
def test_main_block(mock_run):
    mock_run.return_value = type(
        "M",
        (),
        {
            "returncode": 0,
            "stdout": "[()] TA Origin Baseline: 234.0 meters\n[(+)] Dominant Frequency Peak Detected: 59.57 Hz (Magnitude: 0.4568)\n",
            "stderr": "",
        },
    )()
    with patch("sqlite3.connect"):
        runpy.run_module("telemetry_daemon", run_name="__main__")
    mock_run.assert_called()


@patch("subprocess.run")
def test_run_execution_success(mock_run):
    mock_run.return_value = type(
        "M",
        (),
        {
            "returnCode": 0,
            "returncode": 0,
            "stdout": "[()] TA Origin Baseline: 234.0 meters\n[(+)] Dominant Frequency Peak Detected: 59.57 Hz (Magnitude: 0.4568)\n",
            "stderr": "",
        },
    )()
    with patch("sqlite3.connect") as mock_sql:
        mock_conn = MagicMock()
        mock_sql.return_value = mock_conn
        result = telemetry_daemon.run()
        assert isinstance(result, dict)
        assert result["ta_origin"] == 234.0


@patch("subprocess.run")
def test_run_execution_octave_error(mock_run):
    mock_run.return_value = type(
        "M", (), {"returncode": 1, "stdout": "k", "stderr": "Octave error"}
    )()
    with pytest.raises(RuntimeError):
        telemetry_daemon.parse_octave_stream()
