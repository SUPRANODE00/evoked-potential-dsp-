import numpy as np

from sap_filter import SAPReserveProcessFilter


def test_sap_filter_processing():
    sample_rate = 100
    target_freq = 5
    filter_node = SAPReserveProcessFilter(sample_rate, target_freq)

    # Process initial packet
    val, phase = filter_node.process_telemetry(raw_value=1.0, delta_time=0.01)
    assert isinstance(val, (float, np.floating))
    assert isinstance(phase, (float, np.floating))

    # Fill kernel buffer to trigger matrix integration branch
    for _ in range(10):
        output, phase_acc = filter_node.process_telemetry(
            raw_value=0.5, delta_time=0.01
        )

    assert len(filter_node.buffer) == len(filter_node.kernel)
    assert phase_acc > 0.0
