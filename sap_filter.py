import numpy as np

class SAPReserveProcessFilter:
    def __init__(self, sample_rate, target_freq):
        self.sample_rate = sample_rate
        self.target_freq = target_freq
        
        # 1. Time-Domain Decoupling Parameters (PLL Tracking)
        self.phase_accumulator = 0.0
        self.pll_loop_gain = 0.05
        self.last_packet_delta = 0.0
        
        # 2. Attenuation & Cutoff Matrix (Low-pass smoothing)
        rc = 1.0 / (2 * np.pi * target_freq)
        dt = 1.0 / sample_rate
        self.alpha = dt / (rc + dt)
        self.filtered_state = 0.0

        # 3. Continuity Kernel Re-weighting Coefficients (Gaussian Window)
        kernel_size = 5
        sigma = 1.0
        x = np.linspace(-2, 2, kernel_size)
        raw_kernel = np.exp(-x**2 / (2 * sigma**2))
        self.kernel = raw_kernel / np.sum(raw_kernel)
        self.buffer = []

    def process_telemetry(self, raw_value, packet_delta):
        """Executes full filter spectrum on an incoming telemetry node packet."""
        # Vector 1: Time-Domain Decoupling / Phase Adjustment
        self.last_packet_delta = packet_delta
        expected_phase = 2 * np.pi * self.target_freq * packet_delta
        phase_error = expected_phase - self.phase_accumulator
        self.phase_accumulator += expected_phase + (self.pll_loop_gain * phase_error)
        
        # Vector 2: Attenuation & Low-Pass Cutoff
        self.filtered_state = (self.alpha * raw_value) + ((1 - self.alpha) * self.filtered_state)
        
        # Vector 3: Kernel Re-weighting (Buffer Window Tracking)
        self.buffer.append(self.filtered_state)
        if len(self.buffer) > len(self.kernel):
            self.buffer.pop(0)
            
        if len(self.buffer) == len(self.kernel):
            integrated_signal = np.dot(self.buffer, self.kernel)
            return integrated_signal, self.phase_accumulator
            
        return self.filtered_state, self.phase_accumulator

if __name__ == "__main__":
    print("Initializing SAP Reserve Filter Node...")
    sample_rate = 100  # Hz
    target_freq = 5    # Hz
    filter_node = SAPReserveProcessFilter(sample_rate=sample_rate, target_freq=target_freq)
    
    print("\nProcessing simulated packet stream:")
    print(f"{'Packet':<8}{'Raw Val':<10}{'Delta t':<10}{'Filtered Out':<15}{'Phase Accum':<12}")
    print("-" * 55)
    
    np.random.seed(42)
    base_dt = 1.0 / sample_rate
    
    for i in range(1, 11):
        raw_val = np.sin(2 * np.pi * target_freq * (i * base_dt)) + np.random.normal(0, 0.2)
        jittered_dt = base_dt + np.random.normal(0, 0.002) 
        output, phase = filter_node.process_telemetry(raw_val, jittered_dt)
        print(f"{i:<8}{raw_val:<10.4f}{jittered_dt:<10.4f}{output:<15.4f}{phase:<12.4f}")
