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
import numpy as np
import matplotlib.pyplot as plt
from icecube_tools.utils.data import RealEvents
from icecube_tools.point_source_likelihood.point_source_likelihood import PointSourceLikelihood, TimeDependentPointSourceLikelihood
from icecube_tools.point_source_likelihood.energy_likelihood import MarginalisedIntegratedEnergyLikelihood
from icecube_tools.point_source_likelihood.spatial_likelihood import EventDependentSpatialGaussianLikelihood
from icecube_tools.detector.detector import IceCube, TimeDependentIceCube
from icecube_tools.source.flux_model import PowerLawFlux
from icecube_tools.source.source_model import DiffuseSource
from icecube_tools.simulator import TimeDependentSimulator, Simulator
```

## Validating that the background index reconstruction works
```
for index in index_list:
    simulate
    fit
    compare

```

```python
reco_index = []
err_l = []
err_h = []
PERIOD = "IC86_I"
index_list = np.arange(2., 4.1, step=0.5)
SOURCE_DEC = 0
BANDWIDTH = 10
N = 100
for c, index in enumerate(index_list):
    diff_pl = PowerLawFlux(1e-19, 1e5, index, lower_energy=1e2, upper_energy=1e8)
    diffuse_source = DiffuseSource(diff_pl)
    detector = IceCube.from_period(PERIOD)
    #sim = TimeDependentSimulator(["IC86_I", PERIOD], [diffuse_source])
    sim = Simulator(diffuse_source, detector, PERIOD)
    #only around the equator
    sim.max_cosz = np.cos(np.pi / 2 - np.deg2rad(SOURCE_DEC + BANDWIDTH))
    sim.min_cosz = np.cos(np.pi / 2 - np.deg2rad(SOURCE_DEC - BANDWIDTH))
    

    sim.run(show_progress=True, N=N, seed=123456)
    #print(np.log10((sim.reco_energy[PERIOD].min(), sim.reco_energy[PERIOD].max())))
    #print(np.log10(sim.reco_energy[PERIOD]))
    spatial = EventDependentSpatialGaussianLikelihood(20)
    source_coords = (np.pi, np.deg2rad(SOURCE_DEC))
    #mask = np.nonzero((sim.reco_energy[PERIOD] >= np.power(10, 3.2)))
    #sim.mask = {PERIOD: mask}
    energy = MarginalisedIntegratedEnergyLikelihood(
        detector,
        np.linspace(np.log10(sim.reco_energy[PERIOD].min()), np.log10(sim.reco_energy[PERIOD].max()), 20),
        max_index=5.)
    likelihood = PointSourceLikelihood(
        spatial,
        energy,
        sim.ra[PERIOD],
        sim.dec[PERIOD],
        sim.reco_energy[PERIOD],
        sim.ang_err[PERIOD],
        source_coords
    )
    '''
    likelihood = TimeDependentPointSourceLikelihood(
        source_coords,
        ["IC86_I", PERIOD],
        sim.ra,
        sim.dec,
        sim.reco_energy,
        sim.ang_err,
        times={"IC86_I": 1, PERIOD: 1}
    )
    '''
    m = likelihood._minimize_bg()
    m.minos()
    err_l.append(m.merrors["index_atmo"].lower)
    err_h.append(m.merrors["index_atmo"].upper)
    reco_index.append(m.values["index_atmo"])

```

```python
fig, ax = plt.subplots()
ax.errorbar(index_list, reco_index, yerr=(-np.array(err_l), err_h), fmt='+', capsize=5)
x = np.linspace(1.9, 4.1, num=1000)
ax.plot(x, x)
ax.set_aspect("equal")
ax.set_xlabel("true index")
ax.set_ylabel("fitted index")
ax.set_title("{} events, ${}^\circ < \delta < {}^\circ$, {}".format(
    N, SOURCE_DEC-BANDWIDTH, SOURCE_DEC+BANDWIDTH, PERIOD)
)

```

```python
reco_index
```

```python
spatial = EventDependentSpatialGaussianLikelihood(20)
source_coords = (np.pi, 0)
detector = IceCube.from_period("IC86_II")
energy = MarginalisedIntegratedEnergyLikelihood(detector, np.linspace(1, 9, 25), max_index=5.)
likelihood = PointSourceLikelihood(
    spatial,
    energy,
    sim.ra["IC86_II"],
    sim.dec["IC86_II"],
    sim.reco_energy["IC86_II"],
    sim.ang_err["IC86_II"],
    source_coords
)
m = likelihood._minimize_bg()
m
```

```python
_ = m.draw_profile("index_atmo", bound=(1.5, 5.0))
```

```python
events = RealEvents.from_event_files("IC86_II")
detector = IceCube.from_period("IC86_II")
spatial = EventDependentSpatialGaussianLikelihood()
energy = MarginalisedIntegratedEnergyLikelihood(
    detector,
    np.linspace(1, 9, num=25),
    max_index=5.
)
```

```python
likelihood = PointSourceLikelihood(
    spatial,
    energy,
    events.ra[events.periods[0]],
    events.dec[events.periods[0]],
    events.reco_energy[events.periods[0]],
    events.ang_err[events.periods[0]],
    (np.pi, 0),
)
```

```python
m = likelihood._minimize_bg()
```

```python
m
```

```python
_ = m.draw_profile("index_atmo", bound=(1.5, 4.0))
```

```python
tllh = TimeDependentPointSourceLikelihood((np.pi, np.deg2rad(30)), ["IC86_II"], events.ra,
    events.dec, events.reco_energy, events.ang_err, {"IC86_II": energy}, {"IC86_II": 1}
    )
```

```python
tllh._min_index = 1.5
tllh._max_index = 4.0
tllh._minimize_bg()
```

```python
tirf = TimeDependentIceCube.from_periods("IC86_II", "IC86_I")
```

```python
tirf["IC86_II"]
```

```python
type(tirf._detectors)
```

```python

```
