import numpy as np
import scipy.signal as signal

def initialize_ep_pipeline(sample_rate=250.0):
    nyquist = 0.5 * sample_rate
    b_hp, a_hp = signal.butter(4, 0.5 / nyquist, btype='high')
    f0 = 60.0
    Q = 30.0  
    b_notch, a_notch = signal.iirnotch(f0, Q, sample_rate)
    return (b_hp, a_hp), (b_notch, a_notch)

def adaptive_loop_suppression(primary_signal, reference_noise, learning_rate=0.01):
    n_samples = len(primary_signal)
    filter_order = 32
    weights = np.zeros(filter_order)
    clean_output = np.zeros(n_samples)
    padded_ref = np.concatenate((np.zeros(filter_order - 1), reference_noise))
    for i in range(n_samples):
        x = padded_ref[i:i + filter_order][::-1]
        loop_prediction = np.dot(weights, x)
        error = primary_signal[i] - loop_prediction
        clean_output[i] = error
        weights += 2 * learning_rate * error * x
    return clean_output
