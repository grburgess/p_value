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
import h5py
import matplotlib.pyplot as plt
import healpy as hp
from healpy import projview
```

```python
OUTPUT_FILE_BASE = "results/parallel_output_"
```

```python
i = 0
ts = []
while True:
    try:
        with h5py.File(OUTPUT_FILE_BASE+"{}.hdf5".format(i), "r") as f:
            print("file opened")
            i += 1

            ts.append(f["output/ts"][()])
    except FileNotFoundError as e:
        print(e)
        break

ts = np.hstack(ts)
```

```python
projview(
    ts,
    coord=["G"],
    graticule=True,
    graticule_labels=True,
    unit="TS",
    xlabel="ra",#
    ylabel="dec",
    min=0,
    max=ts.max(),
    cmap='viridis',
    cb_orientation="vertical",
    projection_type="aitoff",
);
plt.xticks(color="white")
plt.grid(ls=':')
```

```python

```
