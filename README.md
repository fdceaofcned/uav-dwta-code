# CAS-DWTA laser environment (partial release)

This repository contains part of the simulation environment used in the paper
"An Observe-Orient-Decide-Act-Guided Multi-Agent Deep Reinforcement Learning
Framework for Cooperative UAV Weapon-Target Assignment".

Owing to national defense confidentiality restrictions, only part of the source
code can be released. The released modules are listed below. The remaining code,
including the engagement dynamics, the sensor models, the remaining terms of the
laser propagation model, and the learning algorithms, is available from the
corresponding author upon reasonable request, subject to the applicable
confidentiality restrictions.

## Contents

| Module | Function | Paper reference |
|---|---|---|
| `atmosphere.py` | `standard_atmosphere` | Speed of sound and air density (U.S. Standard Atmosphere 1976) |
| `laser_propagation.py` | `beam_jitter_radius` | Jitter spot radius a_j in Eq. (A6) |
| `laser_propagation.py` | `delivered_power_density` | Delivered power density I, Eq. (A6) |

The atmospheric transmission coefficient, the diffraction spot radius, the
turbulence spot radius, and the thermal-blooming distortion parameter enter
`delivered_power_density` as inputs.

## Experimental configuration

`config/experiment_config.yaml` lists the experimental configuration of the
paper, including the software environment, the computational resources, the
scenario definition of Section 6.1.1, and the parameters in Tables B.1 to B.4.

The scenario considers a 60 km × 60 km contested airspace, in which a formation
of N UAVs (N ∈ {4, 6, 8}) conducts a combat mission against a layered threat
environment. Static hostile sites are located 10 km from the target point, and
mobile hostile sites patrol within a 5 km radius at a standoff distance of
40 km, with their initial positions randomly distributed along the patrol
routes.

## Units

* Laser output power in kW
* Range in km and altitude in m at the function interface
* Spot radii in cm, so that the delivered power density is in kW/cm^2

## Parameters

The parameter values follow Tables B.1 to B.3 of the paper.

## Requirements

Python 3.12 and NumPy 2.1 (see `requirements.txt`). See `example.py` for a minimal usage example.
