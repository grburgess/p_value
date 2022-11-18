from icecube_tools.utils.data import RealEvents
from icecube_tools.point_source_analysis.point_source_analysis import MapScan

events = RealEvents.from_event_files()
#events = RealEvents.from_event_files("IC86_I")
scan = MapScan("config.yaml", events, "output.hdf5")

#scan.nside = 1
scan.generate_sources()
npix = scan.npix
max_fits = 500
starts = []
stops = []
i = 0
while True:
    try:
        if starts[-1] >= npix - max_fits:
            break
    except IndexError:
        pass
    starts.append(i*max_fits)
    if (i+1)*max_fits> npix:
        stops.append(npix)
    else:
        stops.append((i+1)*max_fits)
    i+=1
starts, stops
print(starts, stops)


for c, (l, u) in enumerate(zip(starts, stops)):
    scan.ra_test = None
    scan.dec_test = None
    scan.generate_sources()
    scan.ra_test = scan.ra_test[l:u]
    scan.dec_test = scan.dec_test[l:u]
    scan.write_config("input_configs/parallel_{}.yaml".format(c), source_list=True)