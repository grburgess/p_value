---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.8
  kernelspec:
    display_name: Python 3.9.13 ('icecube_dev')
    language: python
    name: python3
---

```python
from icecube_tools.utils.data import RealEvents, available_periods
from matplotlib import pyplot as plt
from healpy import projview
import numpy as np
```

```python
events = RealEvents.from_event_files(*available_periods, "IC86_III", "IC86_IV", "IC86_V", "IC86_VI", "IC86_VII")
```

```python
# plot distributon of events for each hemisphere

fig, ax = plt.subplots()
north = []
eq = []
south = []
for p in events.periods:
    north.append(events.reco_energy[p][np.nonzero(events.dec[p] >= np.deg2rad(10))])
    eq.append(events.reco_energy[p][np.nonzero((events.dec[p] < np.deg2rad(10)) & (events.dec[p] > np.deg2rad(-10)))])
    south.append(events.reco_energy[p][np.nonzero(events.dec[p] <= np.deg2rad(-10))])

for region, data in zip(["north", "equator", "south"], [north, eq, south]):
    data = np.concatenate(data)
    n, bins, p = ax.hist(data, bins=20, label=region, alpha=0.2)
    n = np.flip(np.cumsum(np.flip(n)))
    n = np.concatenate((np.array([n[0]]), n))
    ax.step(bins, n, color=p[0].get_facecolor(), alpha=1)
    ax.vlines((np.sort(data)[-1000]), 0, 1e6, color='black', ls=':')




textstr = "solid lines: cumulative, but starting at highest energy"
props = dict(boxstyle='round', facecolor='white', alpha=1)

# place a text box in upper left in axes coords
ax.text(1, 1, textstr, fontsize=10,
        verticalalignment='bottom', bbox=props)

ax.set_yscale("log")
ax.set_xlabel("$\log_{10}(E/\mathrm{GeV})$")
ax.set_ylabel("number of events")
ax.legend()
fig.savefig("event_numbers.png", dpi=150)
```

```python

```
