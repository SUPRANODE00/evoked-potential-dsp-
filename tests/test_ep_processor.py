import runpy
from unittest.mock import patch

import pytest

import ep_processor


def test_process_signal_stream_single_iteration():
    with (
        patch("time.sleep", side_effect=InterruptedError("Loop exit")),
        pytest.raises(InterruptedError),
    ):
        ep_processor.process_signal_stream()


def test_ep_processor_main_execution():
    with (
        patch("time.sleep", side_effect=InterruptedError("Main exit")),
        pytest.raises(InterruptedError),
    ):
        runpy.run_module("ep_processor", run_name="__main__")
