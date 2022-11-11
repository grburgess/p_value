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
import matplotlib.pyplot as plt
import numpy as np
import healpy as hp
from healpy import projview

from icecube_tools.utils.data import RealEvents, SimEvents
from icecube_tools.point_source_analysis.point_source_analysis import MapScan
```

```python
#events = RealEvents.from_event_files("IC86_II")
events = SimEvents.load_from_h5("/Users/David/Documents/phd/icecube/icecube_tools/docs/markdown/h5_test.hdf5")
```

```python
scan = MapScan("scan.yaml", events)
```

```python
scan.apply_cuts()
```

```python
scan.generate_sources()
```

```python
scan.ra_test.size
```

```python
scan.perform_scan(show_progress=True)
```

```python
scan.ts.max()
```

```python
projview(
    scan.ts,
    coord=["G"],
    graticule=True,
    graticule_labels=True,
    unit="p value",
    xlabel="ra",
    ylabel="dec",
    min=0,
    max=scan.ts.max(),
    cmap='viridis',
    cb_orientation="vertical",
    projection_type="aitoff",
);
plt.xticks(color="white")
plt.grid(ls=':')
plt.savefig("test_data.png")
```

```python

```
