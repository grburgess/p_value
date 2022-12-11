# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.0
#   kernelspec:
#     display_name: Python 3.9.13 ('icecube_dev')
#     language: python
#     name: python3
# ---

import numpy as np
import h5py
import matplotlib.pyplot as plt
import healpy as hp
from healpy import projview, newprojplot, cartview
print("imported")

OUTPUT_FILE_BASE = "results/parallel_output_"

# +
i = 0
ts = []
ra = []
dec = []

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
    except FileNotFoundError as e:
        #print(e)
        #break
        ts.append(np.zeros(1024))
        

ts = np.hstack(ts)
dec = np.hstack(dec)
ra = np.hstack(ra)
# -

with h5py.File("../ngc_1068/skymap_ngc_restricted.hdf5", "r") as f:
    ts_ngc = f["output/ts"][()]
    ra_ngc = f["meta/ra"][()]
    dec_ngc = f["meta/dec"][()]

projview(
    ts,
    coord=["E"],
    graticule=True,
    graticule_labels=True,
    unit="TS",
    xlabel="ra",
    ylabel="dec",
    min=0,
    max=ts_ngc.max(),
    cmap='viridis',
    cb_orientation="vertical",
    projection_type="aitoff",
    #lonra=[38, 42],
    #latra=[-2, 2]
);
#newprojplot(theta=np.pi/2, phi=np.deg2rad(40.), marker="o", color="r", markersize=2);
plt.xticks(color="white")
plt.grid(ls=':')
#plt.savefig("nside_16.png")

ra[1563], dec[1563]

plt.scatter(ra_ngc, dec_ngc, c=ts_ngc)
plt.xlim(*np.deg2rad([38, 40]))
plt.ylim(*np.deg2rad([-2, 2]))

values = np.zeros(hp.nside2npix(16))
index = hp.ang2pix(16, 40, 0, lonlat=True)
values[index] = 1
map = projview(
    values,
    coord=["E"],
    graticule=True,
    graticule_labels=True,
    unit="TS",
    xlabel="ra",#
    ylabel="dec",
    min=0,
    max=1,
    cmap='viridis',
    cb_orientation="vertical",
    projection_type="aitoff",
);
newprojplot(theta=np.pi/2, phi=np.deg2rad(40.), marker="o", color="r", markersize=2);
plt.xticks(color="white")
plt.grid(ls=':')

plt.show()
