import core.filters as filters


def test_initialize_ep_pipeline():
    hp, notch = filters.initialize_ep_pipeline(sample_rate=250.0)
    assert len(hp[0]) == 3
    assert len(notch[0]) == 3


def test_adaptive_loop_suppression():
    primary_signal = [1.0, 0.5, -0.5, -1.0] * 10
    reference_noise = [0.1, 0.2, -0.1, -0.2] * 10

    clean_output = filters.adaptive_loop_suppression(
        primary_signal, reference_noise, learning_rate=0.01
    )

    assert len(clean_output) == len(primary_signal)
    assert isinstance(clean_output[0], float)
