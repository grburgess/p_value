from icecube_tools.point_source_analysis.point_source_analysis import MapScan
from icecube_tools.utils.data import RealEvents
import numpy as np
import sys

num = sys.argv[1]    # $1 from sky_scan.sh, enumerates configs
CONFIG_FILE = "/home/iwsatlas1/kuhlmann/icecube/p_value/sky_scan/parallel_{}.yaml".format(num)
OUTPUT_FILE = "/home/iwsatlas1/kuhlmann/icecube/p_value/sky_scan/results/parallel_output_{}.hdf5".format(num)

events = RealEvents.from_event_files()   # load all periods

scan = MapScan(CONFIG_FILE, events)
scan.generate_sources()
scan.perform_scan(show_progress=True)
scan.write_output(OUTPUT_FILE, source_list=True)