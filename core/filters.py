import math


def initialize_ep_pipeline(sample_rate=250.0):
    """
    Pure Python implementation of digital signal processing filters.
    Returns tracking coefficients instead of scipy arrays.
    """
    # 60Hz Notch Filter calculation using direct pole-zero mapping
    f0 = 60.0
    w0 = 2.0 * math.pi * f0 / sample_rate
    q = 30.0
    bw = w0 / q

    # Calculate IIR notch coefficients manually
    alpha = math.sin(bw) / 2.0
    b0 = 1.0
    b1 = -2.0 * math.cos(w0)
    b2 = 1.0
    a0 = 1.0 + alpha
    a1 = -2.0 * math.cos(w0)
    a2 = 1.0 - alpha

    notch_b = [b0 / a0, b1 / a0, b2 / a0]
    notch_a = [1.0, a1 / a0, a2 / a0]

    # Simple High-pass (0.5 Hz target) coefficient mapping
    rc = 1.0 / (2.0 * math.pi * 0.5)
    dt = 1.0 / sample_rate
    alpha_hp = rc / (rc + dt)

    hp_b = [alpha_hp, -alpha_hp, 0.0]
    hp_a = [1.0, -(2.0 * alpha_hp - 1.0), 0.0]

    return (hp_b, hp_a), (notch_b, notch_a)


def adaptive_loop_suppression(primary_signal, reference_noise, learning_rate=0.01):
    """Pure Python adaptive filter loop utilizing LMS optimization."""
    n_samples = len(primary_signal)
    filter_order = 32
    weights = [0.0] * filter_order
    clean_output = [0.0] * n_samples

    # Create a padded reference buffer
    padded_ref = [0.0] * (filter_order - 1) + list(reference_noise)

    for i in range(n_samples):
        # Extract and reverse the reference window array
        x = padded_ref[i : i + filter_order][::-1]

        # Calculate dot product
        loop_prediction = sum(w * xi for w, xi in zip(weights, x, strict=False))

        # Calculate the error metrics
        error = primary_signal[i] - loop_prediction
        clean_output[i] = error

        # Update filter taps using the learning rate parameter
        for j in range(filter_order):
            weights[j] += 2.0 * learning_rate * error * x[j]

    return clean_output
