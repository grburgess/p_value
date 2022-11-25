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
from icecube_tools.utils.data import RealEvents, Uptime
from icecube_tools.point_source_likelihood.point_source_likelihood import PointSourceLikelihood, TimeDependentPointSourceLikelihood
from icecube_tools.point_source_likelihood.energy_likelihood import MarginalisedIntegratedEnergyLikelihood
from icecube_tools.point_source_likelihood.spatial_likelihood import EventDependentSpatialGaussianLikelihood
from icecube_tools.detector.detector import IceCube, TimeDependentIceCube
from icecube_tools.source.flux_model import PowerLawFlux
from icecube_tools.source.source_model import DiffuseSource
from icecube_tools.simulator import TimeDependentSimulator, Simulator
from icecube_tools.detector.effective_area import EffectiveArea

```

```python
uptime = Uptime()
times = uptime.time_obs("IC86_I", "IC86_II")
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
PERIODS = ["IC86_I", "IC86_II"]
index_list = np.arange(2., 4.1, step=0.5)
SOURCE_DEC = 0
BANDWIDTH = 10
N = 100
fig, ax = plt.subplots()

for c, index in enumerate(index_list):
    diff_pl = PowerLawFlux(1e-19, 1e5, index, lower_energy=1e2, upper_energy=1e5)
    diffuse_source = DiffuseSource(diff_pl)
    sim = TimeDependentSimulator(["IC86_I", "IC86_II"], [diffuse_source])
    sim.time = times
    #sim = Simulator(diffuse_source, detector, PERIOD)
    #only around the equator
    sim.max_cosz = np.cos(np.pi / 2 - np.deg2rad(SOURCE_DEC + BANDWIDTH))
    sim.min_cosz = np.cos(np.pi / 2 - np.deg2rad(SOURCE_DEC - BANDWIDTH))
    

    sim.run(show_progress=True, seed=123456)
    #print(np.log10((sim.reco_energy[PERIOD].min(), sim.reco_energy[PERIOD].max())))
    #print(np.log10(sim.reco_energy[PERIOD]))
    spatial = EventDependentSpatialGaussianLikelihood(20)
    source_coords = (np.pi, np.deg2rad(SOURCE_DEC))
    #mask = np.nonzero((sim.reco_energy[PERIOD] >= np.power(10, 3.2)))
    #sim.mask = {PERIOD: mask}
    for offset, c, p in zip([-0.07, +0.07], ["red", "blue"], PERIODS):
        detector = IceCube.from_period(p)
    
        energy = MarginalisedIntegratedEnergyLikelihood(
            detector,
            np.linspace(1, 9, 25),
            max_index=5.)
        
        likelihood = PointSourceLikelihood(
            spatial,
            energy,
            sim.ra[p],
            sim.dec[p],
            sim.reco_energy[p],
            sim.ang_err[p],
            source_coords
        )
        m = likelihood._minimize_bg()
        m.minos()
        #_ = m.draw_profile("index_atmo", bound=(1.5, 4))
        #plt.show()

        ax.errorbar(index+offset, m.values["index_atmo"],
            yerr=np.array([[-m.merrors["index_atmo"].lower], [m.merrors["index_atmo"].upper]]),
            fmt='+', capsize=5, color=c)
        
    
    tllh = TimeDependentPointSourceLikelihood(
        source_coords,
        ["IC86_I", "IC86_II"],
        sim.ra,
        sim.dec,
        sim.reco_energy,
        sim.ang_err,
        times=times
    )
    #tllh.likelihoods[p] = likelihood
    
    m = tllh._minimize_bg()
    m.minos()
    ax.errorbar(index, m.values["index_atmo"], yerr=np.array([[-m.merrors["index_atmo"].lower], [m.merrors["index_atmo"].upper]]),
        fmt='+', capsize=5, color='black'
    )
    #_ = m.draw_profile("index_atmo", bound=(1.5, 4))
    #plt.show()

x = np.linspace(1.9, 4.1, num=1000)
ax.plot(x, x)
ax.set_aspect("equal")
ax.set_xlabel("true index")
```

```python
fig, ax = plt.subplots()
ax.errorbar(index_list, reco_index, yerr=(-np.array(err_l), err_h), fmt='+', capsize=5, color="green")
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
PERIODS = ["IC86_I", "IC86_II"]
index_list = np.arange(2., 4.1, step=0.5)
SOURCE_DEC = 0
BANDWIDTH = 10
N = 100
#sim = Simulator(diffuse_source, detector, PERIOD)
#only around the equator


#create output array
num_of_sims = 10

output = np.zeros((len(index_list), 3, num_of_sims))       #  #indices, # values (best fitting, error low, error high), #number of sims
for c, index in enumerate(index_list):
    diff_pl = PowerLawFlux(1e-19, 1e5, index, lower_energy=1e2, upper_energy=1e8)
    diffuse_source = DiffuseSource(diff_pl)
    sim = TimeDependentSimulator(["IC86_I", "IC86_II"], [diffuse_source])
    sim.time = times
    sim.max_cosz = np.cos(np.pi / 2 - np.deg2rad(SOURCE_DEC + BANDWIDTH))
    sim.min_cosz = np.cos(np.pi / 2 - np.deg2rad(SOURCE_DEC - BANDWIDTH))
    for i in range(num_of_sims):


        # run sim
        sim.run(show_progress=True, seed=i, N={p: N for p in PERIODS})
        source_coords = (np.pi, np.deg2rad(SOURCE_DEC))

        # create likelihood and run the fit
        tllh = TimeDependentPointSourceLikelihood(
            source_coords,
            ["IC86_I", "IC86_II"],
            sim.ra,
            sim.dec,
            sim.reco_energy,
            sim.ang_err,
            times=times,
            sigma=5.,
            band_width_factor=3.,
            max_index=4.5
        )

        m = tllh._minimize_bg()
        m.minos()

        # store results for subsequent plotting
        output[c, 0, i] = m.values["index_atmo"]
        output[c, 1, i] = -m.merrors["index_atmo"].lower
        output[c, 2, i] = m.merrors["index_atmo"].upper

```

```python
output = np.load("equator_background_index.npy")
```

```python
index_list = np.arange(2., 4.1, step=0.5)
```

```python
fig, ax = plt.subplots()
for c, index in enumerate(index_list):
    ax.errorbar(np.linspace(index-.1, index+.1, 10), output[c, 0, :], yerr=np.array([[output[c, 1, :]], [output[c, 2, :]]]).squeeze(), fmt="+", capsize=5)
x = np.linspace(1.9, 4.1)
ax.plot(x, x)
ax.set_aspect("equal")
ax.set_xlabel("true index")
ax.set_ylabel("fitted index")
```

```python
np.save("equator_background_index.npy", output)
```

```python

```
