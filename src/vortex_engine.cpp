#include <iostream>
#include <cmath>
#include <string>
#include <iomanip>

struct Vector3D {
    double x, y, z;
};

struct CapsuleState {
    std::string node_id;
    Vector3D enu_coordinates;
    double center_freq_mhz;
    double cancellation_metric;
    std::string lock_status;
};

class CrossTwinVortexEngine {
private:
    CapsuleState primary_temple;
    CapsuleState shadow_agent;

public:
    CrossTwinVortexEngine(std::string origin_id, double lat, double lon, double alt) {
        primary_temple.node_id = origin_id + "_TEMPLE_FRONTEND";
        primary_temple.enu_coordinates = {lat, lon, alt};
        primary_temple.center_freq_mhz = 2400.0;
        primary_temple.cancellation_metric = 0.0;
        primary_temple.lock_status = "LOCKED";

        shadow_agent.node_id = origin_id + "_STAR_BACKEND";
        shadow_agent.enu_coordinates = {-lat, -lon, -alt};
        shadow_agent.center_freq_mhz = 2400.0;
        shadow_agent.cancellation_metric = -100.0;
        shadow_agent.lock_status = "SYNCHRONIZED";
    }

    double compute_vortex_vorticity(double amplitude, double phase_deg) {
        double rad = phase_deg * (M_PI / 180.0);
        double curl_v1 = amplitude * std::cos(rad);
        double curl_v2 = -amplitude * std::cos(rad);
        return curl_v1 + curl_v2;
    }

    void execute_alnitak_alignment(double amp) {
        double net_vorticity = compute_vortex_vorticity(amp, 180.0);
        primary_temple.cancellation_metric = -std::abs(amp * primary_temple.center_freq_mhz);
        
        std::cout << std::fixed << std::setprecision(4);
        std::cout << "=== O'ZONE CAPSULE CROSS-TWIN VORTEX ENGINE ===" << std::endl;
        std::cout << "Frontend Node      : " << primary_temple.node_id << std::endl;
        std::cout << "Backend Shadow Node : " << shadow_agent.node_id << std::endl;
        std::cout << "ENU Origin Anchor   : [" << primary_temple.enu_coordinates.x 
                  << ", " << primary_temple.enu_coordinates.y 
                  << ", " << primary_temple.enu_coordinates.z << "]" << std::endl;
        std::cout << "Net Vortex Curl     : " << net_vorticity << " (Zero-Ground Balance)" << std::endl;
        std::cout << "Cancellation Metric : " << primary_temple.cancellation_metric << " dBm" << std::endl;
        std::cout << "Detachment Status   : " << primary_temple.lock_status << std::endl;
    }
};

int main() {
    CrossTwinVortexEngine engine("SUPRANODE00", 29.6083, -95.2289, 12.0);
    engine.execute_alnitak_alignment(1.5);
    return 0;
}
