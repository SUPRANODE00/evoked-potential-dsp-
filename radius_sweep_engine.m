clear; clc;
rf_nodes = struct('CellID', {137559075, 136815113}, 'PCI', {241, 462}, 'Band', {2, 2}, 'EARFCN', {1100, 1100}, 'RSRP', {-99, -82}, 'TA_m', {234, 234});
N = 30;
theta_vec = linspace(0, 2*pi, N);
phi_vec = linspace(0, pi, N);
[theta, phi] = meshgrid(theta_vec, phi_vec);
base_radius = mean([rf_nodes.TA_m]);
r = base_radius * ones(N, N);
max_z_scale = 8.9868;
Z = max_z_scale * sin(phi);
X = r .* sin(phi) .* cos(theta);
Y = r .* sin(phi) .* sin(theta);
tiers = 1:9;
multipliers = (3 * tiers).^2;
reciprocating_phase = zeros(N, N, length(tiers));
for k = 1:length(tiers)
    reciprocating_phase(:,:,k) = (Z ./ max_z_scale) * multipliers(k);
end
fprintf('[+] Radius Sweep Engine Initialized.\n');
fprintf('[+] TA Origin: %.1f meters | Surface Array: %dx%d\n', base_radius, N, N);
