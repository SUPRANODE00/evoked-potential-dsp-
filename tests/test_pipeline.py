import math
from core.filters import initialize_ep_pipeline

def manual_iir_filter(b, a, data):
    """Direct Form I implementation of an IIR filter for tracking verification."""
    output = [0.0] * len(data)
    for i in range(len(data)):
        out_val = b[0] * data[i]
        if i >= 1:
            out_val += b[1] * data[i-1] - a[1] * output[i-1]
        if i >= 2:
            out_val += b[2] * data[i-2] - a[2] * output[i-2]
        output[i] = out_val
    return output

def test_pipeline_integrity():
    print("[AXIS] Executing core pipeline verification loop...")
    fs = 250.0
    n_samples = int(fs * 2)
    
    # Synthetic signal creation (5Hz Target + 60Hz interference)
    target_signal = [math.sin(2.0 * math.pi * 5.0 * (i / fs)) for i in range(n_samples)]
    loop_interference = [5.0 * math.sin(2.0 * math.pi * 60.0 * (i / fs)) for i in range(n_samples)]
    noisy_input = [t + l for t, l in zip(target_signal, loop_interference)]
    
    # Extract coefficients from the pure Python architecture
    _, (b_notch, a_notch) = initialize_ep_pipeline(fs)
    
    # Pass signal through manual filter architecture
    filtered_step = manual_iir_filter(b_notch, a_notch, noisy_input)
    
    # Calculate variance manually to check loop attenuation power
    deltas = [f - t for f, t in zip(filtered_step[50:], target_signal[50:])] # Skip filter warmup transient
    mean_delta = sum(deltas) / len(deltas)
    residual_loop_power = sum((d - mean_delta) ** 2 for d in deltas) / len(deltas)
    
    print(f"[METRIC] Computed residual loop variance: {residual_loop_power:.4f}")
    assert residual_loop_power < 0.5, "The manual filter loop failed to isolate the origin."
    print("[SUCCESS] Validation array certified. Tracking parameters stable.")

if __name__ == "__main__":
    test_pipeline_integrity()
