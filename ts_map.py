import numpy as np
from scipy.stats import gaussian_kde, uniform
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib.colors as colors
from healpy.newvisufunc import projview, newprojplot

import healpy as hp

from astropy.coordinates import SkyCoord
from astropy import units as u

from icecube_tools.detector.r2021 import R2021IRF
from icecube_tools.detector.effective_area import EffectiveArea
from icecube_tools.detector.detector import IceCube
from icecube_tools.point_source_likelihood.energy_likelihood import (
    MarginalisedEnergyLikelihood2021,
    MarginalisedIntegratedEnergyLikelihood
)
from icecube_tools.point_source_likelihood.point_source_likelihood import (
    PointSourceLikelihood,
)
from icecube_tools.point_source_likelihood.spatial_likelihood import (
    EventDependentSpatialGaussianLikelihood,
)


def spherical_to_icrs(theta, phi):
    ra = phi
    dec = np.pi / 2 - theta
    return ra, dec

def icrs_to_spherical(ra, dec):
    phi = ra
    theta = np.pi / 2 - dec
    return theta, phi

def spherical_to_cart(r, theta, phi):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z


def add_events(*periods):
    events = []
    for p in periods:
        events.append(np.loadtxt(f"/Users/David/.icecube_data/20210126_PS-IC40-IC86_VII/icecube_10year_ps/events/{p}_exp.csv"))
    return np.concatenate(tuple(events))

def extract_data(events):
    ra = np.deg2rad(events[:, 3])
    dec = np.deg2rad(events[:, 4])
    energy = np.power(10, events[:, 1])
    ang_err = events[:, 2]
    zenith = events[:, -1]
    return ra, dec, ang_err, energy


angular_resolution = 1  # deg
spatial_likelihood = EventDependentSpatialGaussianLikelihood(angular_resolution)
irf = R2021IRF.from_period("IC86_II")
aeff = EffectiveArea.from_dataset("20210126")
reco_bins = irf.reco_energy_bins[-1, 0]
energy_likelihood = MarginalisedIntegratedEnergyLikelihood(irf, aeff, reco_bins)

events = add_events("IC86_II")
events = events[np.nonzero(events[:, 1] >=6)]
ra, dec, ang_err, energy = extract_data(events)


dec_max = dec.max() + np.deg2rad(3.)
dec_min = dec.min() - np.deg2rad(3.)

theta_min, _ = icrs_to_spherical(0, dec_max)
theta_max, _ = icrs_to_spherical(0, dec_min)

coords = SkyCoord(frame='icrs', ra=ra*u.rad, dec=dec*u.rad)
coords.representation_type = "cartesian"

nside = 16
npix = hp.nside2npix(nside)
print("resolution in degrees:", hp.nside2resol(nside, arcmin=True)/60)
theta_test, phi_test = hp.pix2ang(nside, np.arange(npix), nest=False)
ra_test, dec_test = spherical_to_icrs(theta_test, phi_test)

npix = hp.nside2npix(nside)


final_ts = np.zeros(npix)
index = np.zeros(npix)
ns = np.zeros(npix)

for c, source_coord in enumerate(zip(ra_test, dec_test)):
    #set up likelihood object
    if source_coord[1] <= np.deg2rad(10):
        likelihood = PointSourceLikelihood(
            spatial_likelihood,
            energy_likelihood,
            ra,
            dec,
            energy,
            ang_err,
            source_coord,
            which='both'
        )
        if likelihood.N > 0:    # else somewhere division by zero
            ts = likelihood.get_test_statistic()
            index[c] = likelihood._best_fit_index
            ns[c] = likelihood._best_fit_ns
            final_ts[c] = ts

print(final_ts.max())

"""
hpxmap = np.zeros(npix, dtype=np.float)
indices = np.arange(theta_test.size)
for i in range(len(final_ts)):
    hpxmap[indices[i]] = final_ts[i]


N_tests = 100

test_ts = np.zeros((N_tests, npix))

for i in range(N_tests):
    #shuffle RA of events
    ra = uniform.rvs(0, 2*np.pi, size=events.shape[0])   # overwrite with random values
    for c, source_coord in enumerate(zip(ra_test, dec_test)):
        if source_coord[1] <= np.deg2rad(10):
    #set up likelihood object
            likelihood = PointSourceLikelihood(
                spatial_likelihood,
                energy_likelihood,
                ra,
                dec,
                energy,
                ang_err,
                source_coord,
                which='both'
            )
            if likelihood.N > 0:
                ts = likelihood.get_test_statistic()
                # print(likelihood._best_fit_ns)
            else:
                ts = 0.
            test_ts[i, c] = ts
# -

np.save("test_ts.npy", test_ts)

sorted_ts = np.sort(test_ts, axis=0)
p_index = np.zeros(npix)
for i in range(npix):
    p_index[i] = np.searchsorted(sorted_ts[:, i], final_ts[i])

plt.hist(p_index)

p = (100 - p_index + 1) / 100.

# +
hpxmap = np.zeros(npix, dtype=np.float)
for i in range(len(final_ts)):
    hpxmap[indices[i]] = p[i]



"""