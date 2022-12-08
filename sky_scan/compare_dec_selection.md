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

## Declination band selection

Each test source will select according to bandwidth and sigma the source events to include. This is further extended to include the entire aeff declination/cosz band in which the borders lie. This notebook tests whether the selected cosz bins are the same when inserting sources at each cosz band's center to generate the TS distributions.

```python
from icecube_tools.detector.effective_area import EffectiveArea
from icecube_tools.point_source_analysis.point_source_analysis import MapScan
from icecube_tools.utils.coordinate_transforms import spherical_to_icrs
from icecube_tools.point_source_likelihood.point_source_likelihood import PointSourceLikelihood, TimeDependentPointSourceLikelihood
from icecube_tools.utils.data import SimEvents
import healpy as hp
import numpy as np
import matplotlib.pyplot as plt
```

```python
aeff = EffectiveArea.from_dataset("20210126", "IC86_II")
events = SimEvents.load_from_h5("../../icecube_tools/docs/markdown/h5_test.hdf5")
```

```python
!pwd
```

```python
#cosz = -sin(dec), dec = -arcsin(cosz)

cosz = aeff.cos_zenith_bins
dec_bins = -np.arcsin(cosz)
sindec_bins = sorted(-cosz)
```

```python
sindec_bins
```

```python
# aeff_dec_high, aeff_dec_low
dec_limits = []
tllh = TimeDependentPointSourceLikelihood((0, 0), ["IC86_II"], events.ra, events.dec, events.reco_energy, events.ang_err, )
for (dec_low, dec_high) in zip(sindec_bins[:-1], sindec_bins[1:]):
    middle_dec = np.arcsin((2 * dec_low + dec_high) / 3)
    tllh.source_coord = (0, middle_dec)
    llh = tllh.likelihoods["IC86_II"]
    dec_limits.append((llh._dec_low, llh._dec_high))
```

```python
theta, phi = hp.pix2ang(256, np.arange(hp.nside2npix(256)), nest=False)
ra, dec = spherical_to_icrs(theta, phi)
decs_in_hp = sorted(list(set(dec.tolist())))
```

```python

```

```python
dec_limits_in_hp = []
for dec in decs_in_hp:
    if dec > -np.deg2rad(81.) and dec < np.deg2rad(81):
        pass
    else:
        continue
    tllh.source_coord = (0, dec)
    llh = tllh.likelihoods["IC86_II"]
    tup = (llh._dec_low, llh._dec_high)
    dec_limits_in_hp.append(tup)

```

```python
print(dec_limits)
```

```python
len(set(dec_limits_in_hp))
```

```python
dec_bins
```

```python
sindec_bins
```

```python
bandwidth = np.deg2rad(10)    # =/- 10 degrees
```

```python
fig, ax = plt.subplots()

x = np.linspace(-np.pi/2, np.pi/2, 1000)
ax.plot(x, np.sin(x))
lower_bound = np.sin(x-bandwidth)
upper_bound = np.sin(x+bandwidth)
delta_sin = np.abs(cosz[1] - cosz[0])
lower_bound[np.nonzero(((x < 0) & (x - bandwidth < -np.pi/2)))] = -1.
upper_bound[np.nonzero(((x > 0) & (x + bandwidth > np.pi/2)))] = 1.
ax.fill_between(x, lower_bound, upper_bound, alpha=0.3, label="sin(dec +/- 10 degrees)")
ax.fill_between(x, np.sin(x)-8*delta_sin, np.sin(x)+8*delta_sin, alpha=0.3, label="sin(dec) +/- 8 dec bins")
ax.scatter(np.arcsin(sindec_bins), np.zeros_like(sindec_bins), marker="|", s=50, label="dec bins")
ax.scatter(np.zeros_like(sindec_bins), sindec_bins, marker="_", s=50, label="sin(dec) bins")

ax.set_xlabel("dec")
ax.set_ylabel("sin dec")
ax.legend()
ax.set_ylim(-1, 1)
```

```python

```
