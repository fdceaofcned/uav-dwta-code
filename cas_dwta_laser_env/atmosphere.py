"""Standard atmosphere model used in the simulation environment.

The implementation follows the piecewise layer description of the
U.S. Standard Atmosphere 1976 up to a geopotential altitude of 84.852 km.
"""

import math

# Sea-level reference values
RHO_SL = 1.22500        # air density at sea level [kg/m^3]
TEMP_SL = 288.15        # temperature at sea level [K]
R_AIR = 287.053         # specific gas constant of dry air [J/(kg*K)]
GAMMA_AIR = 1.4         # ratio of specific heats of air [-]

# Earth radius used for the geometric-to-geopotential conversion [km]
R_EARTH_KM = 6369.0
# Hydrostatic constant g0 * M0 / R* [K/km]
GMR = 34.163195

# Layer tables: base geopotential altitude [km], base temperature [K],
# base pressure ratio p/p_sl [-], and temperature gradient [K/km]
H_TAB = (0.0, 11.0, 20.0, 32.0, 47.0, 51.0, 71.0, 84.852)
T_TAB = (288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65, 186.946)
P_TAB = (1.0, 2.233611e-1, 5.403295e-2, 8.5666784e-3, 1.0945601e-3,
         6.6063531e-4, 3.9046834e-5, 3.68501e-6)
G_TAB = (-6.5, 0.0, 1.0, 2.8, 0.0, -2.8, -2.0, 0.0)


def _layer_index(h_km):
    """Return the index of the atmospheric layer that contains h_km."""
    i, j = 0, len(H_TAB) - 1
    while j > i + 1:
        k = (i + j) // 2
        if h_km < H_TAB[k]:
            j = k
        else:
            i = k
    return i


def standard_atmosphere(height_m):
    """Speed of sound and air density at a given geometric altitude.

    Parameters
    ----------
    height_m : float
        Geometric altitude above sea level [m].

    Returns
    -------
    speed_of_sound : float
        Speed of sound [m/s].
    density : float
        Air density [kg/m^3].
    """
    alt_km = height_m / 1000.0
    h = alt_km * R_EARTH_KM / (alt_km + R_EARTH_KM)  # geopotential altitude [km]

    i = _layer_index(h)
    t_grad = G_TAB[i]
    t_base = T_TAB[i]
    delta_h = h - H_TAB[i]
    t_local = t_base + t_grad * delta_h

    if t_grad == 0.0:
        delta = P_TAB[i] * math.exp(-GMR * delta_h / t_base)
    else:
        delta = P_TAB[i] * (t_base / t_local) ** (GMR / t_grad)

    theta = t_local / TEMP_SL          # temperature ratio
    sigma = delta / theta              # density ratio

    density = RHO_SL * sigma
    temperature = TEMP_SL * theta
    speed_of_sound = math.sqrt(GAMMA_AIR * R_AIR * temperature)
    return speed_of_sound, density
