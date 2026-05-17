import numpy as np
import scipy.signal as signal
from core.filters import initialize_ep_pipeline

def test_pipeline_integrity():
    fs = 250.0
    t = np.linspace(0, 2, int(fs * 2), endpoint=False)
    target_signal = np.sin(2 * np.pi * 5 * t) 
    loop_interference = 5.0 * np.sin(2 * np.pi * 60 * t)
    noisy_input = target_signal + loop_interference
    (b_hp, a_hp), (b_notch, a_notch) = initialize_ep_pipeline(fs)
    filtered_step = signal.filtfilt(b_notch, a_notch, noisy_input)
    residual_loop_power = np.var(filtered_step - target_signal)
    assert residual_loop_power < 0.5, "The loop suppression filter failed to isolate the origin."
