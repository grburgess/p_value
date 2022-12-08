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
from healpy import projview, newprojplot, cartview, projplot
from astropy.coordinates import SkyCoord
from astropy import units as u
from icecube_tools.point_source_analysis.point_source_analysis import MapScan
from icecube_tools.utils.data import RealEvents
```

```python
for i in range(558, 768):
    scan = MapScan.load_output(f"results/parallel_output_{i}.hdf5", RealEvents.from_event_files())
    if not np.all(scan.fit_ok):
        
        idx = np.nonzero(scan.fit_ok == 0)[0]
        for num in idx:
            print(i, num)
            scan._test_source((scan.ra_test[num], scan.dec_test[num]), num, scan.events.ra, scan.events.dec, scan.events.reco_energy, scan.events.ang_err)
            print(scan.likelihood.m.fmin.is_valid, scan.likelihood.m.values["ns"], scan.likelihood.m.errors["ns"], scan.likelihood.m.values["index"], scan.likelihood.m.errors["index"], )
        scan.write_output(scan.output_path, source_list=True)
```

```python
OUTPUT_FILE_BASE = "results/parallel_output_"
```

```python
i = 0
ts = []
ra = []
dec = []
faulty = []
fit_ok = []
for i in range(768):
    try:
        with h5py.File(OUTPUT_FILE_BASE+"{}.hdf5".format(i), "r") as f:
            #print("file opened")
            #i += 1

            ts.append(f["output/ts"][()])
            ra.append(f["meta/ra"][()])
            dec.append(f["meta/dec"][()])
            fit_ok.append(f["output/fit_ok"][()])
            if np.any(ts[-1][-4:] == 0):
                faulty.append(i)
    except FileNotFoundError as e:
        faulty.append(i)
        #print(e)
        #break
        ts.append(np.zeros(1024))
        

ts = np.hstack(ts)
dec = np.hstack(dec)
ra = np.hstack(ra)
fit_ok = np.hstack(fit_ok)
```

```python
with h5py.File("../ngc_1068/skymap_ngc_restricted.hdf5", "r") as f:
    ts_ngc = f["output/ts"][()]
    ra_ngc = f["meta/ra"][()]
    dec_ngc = f["meta/dec"][()]
```

```python
fig = plt.figure(1, dpi=30)

projview(
    ts,
    coord=["E"],
    graticule=True,
    graticule_labels=True,
    unit="TS",
    xlabel="ra",
    ylabel="dec",
    min=0,
    max=ts.max(),
    cmap='viridis',
    cb_orientation="vertical",
    projection_type="aitoff",
    #lonra=[38, 42],
    #latra=[-2, 2]
    fig=1
);
for f in faulty:
    newprojplot(phi=scan.ra_test[f], theta=scan.dec_test[f], marker='o', color='red', markersize=2)
#newprojplot(phi=0, theta=0, marker='o', color='red')
##phi = np.linspace(0, np.pi, 1000)
# theta = np.full(1000, np.pi/2)
# takes phi, theta as arguments...
#ra = np.linspace(0, 2*np.pi, 1000)*u.rad
#dec = np.full(1000, 0)*u.rad
#coords = SkyCoord(ra, dec, unit="rad", frame="galactic",)
#newprojplot(phi=coords.icrs.ra.value/(2*np.pi), theta=np.pi/2 - coords.icrs.dec.value/(2*np.pi), marker="o", color="r", markersize=2);
plt.xticks(color="white")
plt.grid(ls=':')
plt.savefig("nside_256.png", dpi=150)
```

```python
faulty = np.argwhere(fit_ok == False)
```

```python
faulty
```

```python
scan = MapScan("input_configs/parallel_3.yaml", RealEvents.from_event_files(), "test_output.hdf5")
scan.ra_test = None
scan.dec_test = None
scan.generate_sources()
```

```python
scan.ra_test = np.array([scan.ra_test[1604]])
scan.dec_test = np.array([scan.dec_test[1604]])
```

```python
scan.generate_sources()
```

```python
scan.ra_test.size, scan.dec_test
```

```python
np.pi/2
```

```python
scan.perform_scan(show_progress=True)
```

```python
scan.fit_ok
```

```python
scan.likelihood.m.draw_profile("ns",)
```

```python
scan.ra_test[faulty]
```

```python

```
