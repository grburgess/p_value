from icecube_tools.point_source_analysis.point_source_analysis import MapScan
from icecube_tools.utils.data import RealEvents
import sys

num = sys.argv[1]    # $1 from sky_scan.sh, enumerates configs
print(num)
CONFIG_FILE = "/home/iwsatlas1/kuhlmann/icecube/p_value/sky_scan/input_configs/parallel_{}.yaml".format(num)
print(CONFIG_FILE)
#CONFIG_FILE = sys.argv[1]
#num = CONFIG_FILE.rstrip('.yaml').rsplit("_")[-1]
OUTPUT_FILE = "/home/iwsatlas1/kuhlmann/icecube/p_value/sky_scan/results/parallel_output_{}.hdf5".format(num)

events = RealEvents.from_event_files()   # load all periods

scan = MapScan(CONFIG_FILE, events, OUTPUT_FILE)
scan.generate_sources()
scan.perform_scan(show_progress=False)
scan.write_output(OUTPUT_FILE, source_list=True)
