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
from matplotlib import pyplot as plt
import numpy as np
from icecube_tools.utils.data import RealEvents, Uptime
from icecube_tools.point_source_likelihood.point_source_likelihood import TimeDependentPointSourceLikelihood
from icecube_tools.point_source_likelihood.energy_likelihood import MarginalisedIntegratedEnergyLikelihood
from icecube_tools.simulator import TimeDependentSimulator, Simulator
from icecube_tools.source.source_model import PointSource, DiffuseSource
from icecube_tools.source.flux_model import PowerLawFlux
from icecube_tools.neutrino_calculator import NeutrinoCalculator
from icecube_tools.detector.effective_area import EffectiveArea
from icecube_tools.detector.detector import IceCube
from icecube_tools.detector.r2021 import R2021IRF

```

```python
PERIODS = ["IC86_II"]


events = RealEvents.from_event_files(*PERIODS)
uptime = Uptime()
times = uptime.time_obs(*PERIODS)
aeff = EffectiveArea.from_dataset("20210126", "IC86_II")
irf = R2021IRF.from_period("IC86_II")
icecube = IceCube(aeff, irf, irf)
```

```python
times
```

```python
index = 2.7
min_energy = 1e2
max_energy = 1e8
norm_energy = 1e5
normalisation = 1e-19
flux = PowerLawFlux(normalisation, norm_energy, index, lower_energy=min_energy, upper_energy=max_energy)
# 100TeV = 100e3GeV = 1e5GeV
diff_flux = PowerLawFlux(1.44e-20, 1e5, 3.7, min_energy, max_energy)   # astrophysical
coord = (np.pi, 0)    # equator
ps = PointSource(flux, z=0.0, coord=coord)
diff = DiffuseSource(diff_flux)
sources = [diff, ps]

nu_calc = NeutrinoCalculator(sources, aeff)
print(nu_calc(1, min_energy, max_energy,))


```

```python

sim = Simulator(sources, icecube, "IC86_II")
sim.max_cosz = np.cos(np.deg2rad(80))
sim.run()
```

```python
energy_llh = {"IC86_II": MarginalisedIntegratedEnergyLikelihood(irf, aeff, np.linspace(2, 9, num=25))}
likelihood = TimeDependentPointSourceLikelihood(coord, ["IC86_II"], events.ra, events.dec, events.reco_energy, events.ang_err, energy_llh, times)
```

```python
size = 100
ts = np.zeros(size)
index = np.zeros(size)
ns = np.zeros(size)
for i in range(size):
    events.scramble_ra()
    likelihood = TimeDependentPointSourceLikelihood(coord, ["IC86_II"], events.ra, events.dec, events.reco_energy, events.ang_err, energy_llh, times)
    ts[i] = likelihood.get_test_statistic()
    index[i] = likelihood._best_fit_index
    ns[i] = likelihood._best_fit_ns
```

```python
plt.hist(ts)
```

```python
plt.hist(index)
```

```python
plt.hist(ns)
```

```python
likelihood.get_test_statistic()
```

```python
likelihood._best_fit_index, likelihood._best_fit_ns
```

```python
_ = likelihood.m.draw_profile("ns")
```

```python
_ = likelihood.m.draw_profile("index", bound=(1.5, 3.95))
```

```python
events.ang_err
```

```python

```
