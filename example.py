"""Minimal usage example of the released environment modules."""

import numpy as np

from cas_dwta_laser_env import (
    standard_atmosphere,
    beam_jitter_radius,
    delivered_power_density,
)

np.random.seed(0)

speed_of_sound, density = standard_atmosphere(5000.0)
print(f"Altitude 5 km: speed of sound {speed_of_sound:.2f} m/s, density {density:.4f} kg/m^3")

range_km = 10.0
a_j = beam_jitter_radius(range_km)
print(f"Jitter spot radius a_j = {a_j:.3f} cm")

# Illustrative values for the terms that are supplied as inputs
tau_a, a_d, a_t, n_d = 0.8, 2.0, 1.5, 1.0
intensity = delivered_power_density(50.0, tau_a, a_d, a_j, a_t, n_d, beta_ao=0.5)
print(f"Delivered power density I = {intensity:.4f} kW/cm^2")
