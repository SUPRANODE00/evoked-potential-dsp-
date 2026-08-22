from unittest.mock import patch

import pytest

import ep_processor


def test_butterworth_bandpass_filter():
    data = [10.0, -10.0, 5.0, -5.0]
    filtered = ep_processor.butterworth_bandpass_filter(data)
    assert len(filtered) == len(data)


def test_process_signal_stream_single_iteration():
    # Force time.sleep to raise an exception to exit the infinite loop after 1 cycle
    with patch("time.sleep", side_effect=InterruptedError("Loop exit")):
        with pytest.raises(InterruptedError):
            ep_processor.process_signal_stream()


def test_ep_processor_main_execution():
    import runpy

    # Intercept sleep call when executing as __main__
    with patch("time.sleep", side_effect=InterruptedError("Main exit")):
        with pytest.raises(InterruptedError):
            runpy.run_module("ep_processor", run_name="__main__")
