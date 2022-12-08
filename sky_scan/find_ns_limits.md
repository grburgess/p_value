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
from icecube_tools.point_source_likelihood.point_source_likelihood import TimeDependentPointSourceLikelihood
from icecube_tools.utils.data import RealEvents, Uptime
import numpy as np
```

```python
events = RealEvents.from_event_files()
uptime = Uptime()
```

```python
tllh = TimeDependentPointSourceLikelihood((np.deg2rad(40), 0), events.periods, events.ra, events.dec, events.reco_energy, events.ang_err, times=uptime.time_obs(*events.periods))
```

```python
tllh._calc_weights(2.0)
```

```python
tllh.Nprime_dict, tllh.N_dict, tllh.Ntot_dict
```

```python
min([llh.N for llh in tllh.likelihoods.values()])
```

```python

```
