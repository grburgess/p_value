import matplotlib.pyplot as plt
import numpy as np
import healpy as hp
from healpy import projview
from icecube_tools.utils.data import RealEvents, SimEvents, available_periods
from icecube_tools.point_source_analysis.point_source_analysis import MapScan
import h5py
import yaml


events = RealEvents.from_event_files(*available_periods, "IC86_III", "IC86_IV", "IC86_V", "IC86_VI", "IC86_VII")

scan = MapScan("config.yaml", events)

events.periods

scan.generate_sources()



for i in range(2):
    scan.nside=1
    scan.generate_sources()
    print(scan.npix)
    lower = int(np.floor(i*scan.npix/2))
    upper = int(np.floor((i+1)*scan.npix/2))
    print(lower, upper)
    #scan.ra_test = scan.ra_test[lower:upper]
    #scan.dec_test = scan.dec_test[lower:upper]
    #scan.write_config("parallel_{}.yaml".format(i), source_list=True)