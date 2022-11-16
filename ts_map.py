import numpy as np
from scipy.stats import gaussian_kde, uniform
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib.colors as colors
from healpy.newvisufunc import projview, newprojplot
from time import time
import healpy as hp

from astropy.coordinates import SkyCoord
from astropy import units as u

#import point source /mapscan class
#load instance
#check config writing/loading
#paralellisation?


#for (r, d, num) in zip(ra_test, dec_test, np.arange(npix)):
#    test_source((r, d), num)





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