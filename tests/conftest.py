import os
import pytest


@pytest.fixture(autouse=True)
def cleanup_dsp_log():
    yield
    if os.path.exists("processed_ep.log"):
        os.remove("processed_ep.log")
