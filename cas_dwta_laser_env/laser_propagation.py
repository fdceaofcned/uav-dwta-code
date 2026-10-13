"""Laser propagation components of the simulation environment.

This module provides the beam-jitter spot radius and the delivered power
density of Eq. (A6) in Appendix A of the paper. The atmospheric
transmission coefficient, the diffraction spot radius, the turbulence spot
radius, and the thermal-blooming distortion parameter enter Eq. (A6) as
inputs and are not part of this release.

Unit convention (as used in the experiments)
--------------------------------------------
* Laser output power P0 in kW.
* Engagement range L in km at the function interface.
* Spot radii in cm, so that the delivered power density is in kW/cm^2.
"""

import math

import numpy as np

ARCSEC_TO_RAD = 0.017453293 / 3600.0   # 1 arcsec in rad
KM_TO_CM = 1.0e5


def beam_jitter_radius(range_km, rng=None):
    """Spot-radius expansion caused by beam jitter, a_j in Eq. (A6).

    The jitter angle is drawn as |N(1, 0.01^2)| arcsec at each call, where
    1 arcsec is the aiming error in Table B.1.

    Parameters
    ----------
    range_km : float
        Range between the laser platform and the threat [km].
    rng : numpy.random.Generator, optional
        Random generator. If None, the global NumPy random state is used,
        which is seeded before each run as described in Section 6.1.2.

    Returns
    -------
    float
        Jitter spot radius a_j [cm].
    """
    z = rng.standard_normal() if rng is not None else float(np.random.randn(1)[0])
    jitter_arcsec = abs(z * math.sqrt(0.0001) + 1.0)
    jitter_rad = jitter_arcsec * ARCSEC_TO_RAD
    return jitter_rad * range_km * KM_TO_CM


def delivered_power_density(power_kw, tau_a, a_d, a_j, a_t, n_d, beta_ao):
    """Delivered power density on the threat, Eq. (A6).

    Parameters
    ----------
    power_kw : float
        Laser output power P0 [kW].
    tau_a : float
        Atmospheric transmission coefficient [-].
    a_d, a_j, a_t : float
        Spot-radius expansions caused by diffraction, beam jitter, and
        turbulence [cm].
    n_d : float
        Thermal-blooming distortion parameter [-].
    beta_ao : float
        Adaptive-optics compensation coefficient [-], Table B.1.

    Returns
    -------
    float
        Delivered power density I [kW/cm^2].
    """
    comp = (1.0 - beta_ao) ** 2
    spot_area = math.pi * (a_d ** 2 + a_j ** 2 + comp * a_t ** 2)
    blooming = 1.0 + 0.0625 * comp * n_d ** 2
    return power_kw * tau_a / (spot_area * blooming)
