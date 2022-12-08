---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.0
  kernelspec:
    display_name: Python 3.9.13 ('icecube_dev')
    language: python
    name: python3
---

```python
import matplotlib.pyplot as plt
import numpy as np
import healpy as hp
from healpy import projview
from icecube_tools.utils.data import RealEvents, SimEvents
from icecube_tools.point_source_analysis.point_source_analysis import MapScan, MapScanTSDistribution
import h5py
from scipy.stats import ncx2, chi2
```

## Idea to parallelise in a sensible fashion

Set npix/nside to the desired angular resolution and generate sources. Split sources into reasonable length parts, e.g. 1000 sources, meaning `MapScan().test_ra = MapScan().test_ra[n*1000:(n+1)*1000]`. Then write config with distinct name. Repeat until all sources are in mentioned in a config.

Read in configs in parallel processes, calculate, write output again with same distinct identifier.

Make script reading in all result files.

```python
events = RealEvents.from_event_files()
```

```python
scan = MapScan("config.yaml", events, "skymap_ngc_restricted_updated_dec.hdf5")
```

```python
events.periods
```

```python
r = np.deg2rad(np.linspace(38, 42, num=11))
d = np.deg2rad(np.linspace(-2, 2, num=11))
rr, dd = np.meshgrid(r, d)
rr = rr.flatten()
dd = dd.flatten()
print(rr.size)
```

```python
scan.ra_test = rr
scan.dec_test = dd
scan.generate_sources(nside=False)
scan.ts.shape
```

```python
scan.perform_scan(show_progress=True)
```

```python
fig, ax = plt.subplots()
pcol = ax.pcolormesh(np.rad2deg(r), np.rad2deg(d), scan.ts.reshape((11, 11)), shading="nearest")
fig.colorbar(pcol, ax=ax, label='TS')
ax.scatter(40.6696215289200, -00.0132943583900, c="red")
```

```python
fig, ax = plt.subplots()
pcol = ax.pcolormesh(np.rad2deg(r), np.rad2deg(d), scan.ns.reshape((11, 11)), shading="nearest")
fig.colorbar(pcol, ax=ax, label='ns')
ax.scatter(40.6696215289200, -00.0132943583900, c="red")
```

```python
fig, ax = plt.subplots()
pcol = ax.pcolormesh(np.rad2deg(r), np.rad2deg(d), scan.index.reshape((11, 11)), shading="nearest")
fig.colorbar(pcol, ax=ax, label='index')
ax.scatter(40.6696215289200, -00.0132943583900, c="red")
```

## Create TS distribution
TS values themselves are not calibrated, we need to "simulate" (i.e. for a large enough data set shuffle the RAs to wash out any source associations) lots of events, fit again a source and find the TS. From the number of simulated data sets with TS larger than the one from the un-shuffled data we obtain the local p-value.

Since the declination-dependency is given by the declination dependency of the effective area, it is sufficient to create TS distributions only once for each aeff's declination bin.

```python
ts_dist = MapScanTSDistribution("config.yaml", events, "ts_dist.hdf5")
```

```python
ts_dist.ra_test = np.array([np.pi])
ts_dist.dec_test = np.array([np.deg2rad(-0.3)])
ts_dist.ntrials=1000
```

```python
ts_dist.generate_sources(nside=False)
```

```python
ts_dist.ts.shape
```

```python
ts_dist.perform_scan(show_progress=True)
```

```python
ts_copy = ts_dist.ts.copy()
```

```python
ts_copy.sort()
```

```python
plt.hist(ts_copy, bins=20, density=True, label="1000 simulations")
pars = chi2.fit(ts_copy)
x = np.linspace(0, 80, num=1000)
plt.plot(x, chi2(*pars).pdf(x), label="chi2 fit")
plt.xlabel("TS")
plt.ylabel("pdf")
plt.legend()
print(pars)
```

```python

```
