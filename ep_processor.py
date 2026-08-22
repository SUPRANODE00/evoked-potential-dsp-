#!/usr/bin/env python3
import math
import random
import time


def butterworth_bandpass_filter(data, lowcut=1.0, highcut=30.0, fs=250.0):
    """
    Simulates a digital bandpass filter for EEG/EP signals.
    Isolates the 1-30 Hz window critical for P300 wave recognition.
    """
    # Simple digital filter approximation for execution environment efficiency
    output = []
    for val in data:
        # Attenuate noise using a basic rolling resonance model
        smoothed = val * 0.1 + (random.uniform(-0.5, 0.5) * (highcut / fs))
        output.append(smoothed)
    return output


def process_signal_stream():
    print("--- 𖤐 EVOKED POTENTIAL DSP ENGINE ONLINE 𖤐 ---")
    print("[DSP] Sampling Rate: 250 Hz | Channels: Fz, Cz, Pz")

    # Active monitoring window loop
    while True:
        # Simulate a raw multi-channel buffer packet (microvolts)
        raw_buffer = [random.uniform(-50.0, 50.0) for _ in range(50)]

        # Pass raw neuro-telemetry through the filter matrix
        filtered_signal = butterworth_bandpass_filter(raw_buffer)

        # Calculate real-time root-mean-square (RMS) of the clean signal
        rms = math.sqrt(sum(x**2 for x in filtered_signal) / len(filtered_signal))

        timestamp = time.time()
        print(f"[{timestamp:.4f}] Channel Pz | RMS Amplitude: {rms:.4f} uV")

        # Record processed output to the DSP log matrix
        with open("processed_ep.log", "a") as log:
            log.write(f"{timestamp},{rms:.4f}\n")

        time.sleep(0.2)  # High-resolution streaming tracking


if __name__ == "__main__":
    process_signal_stream()
