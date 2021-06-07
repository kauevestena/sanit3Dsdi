# import pickle
from study_case_config import *
from library import data_fetch as df
import os

# the workflow is mostly the same from "get_data_wfs.py"
# but we create in "checking mode"
wfs_source = df.wfs_data_fetcher(wfs_url,checking_mode=True)
# we do not need to acquire the municipality
wfs_source.get_interest_list_of_layers(interest_layers_keystring)
wfs_source.compile_and_dump_interest_infos(only_compile=True) # we use the "only compile" switch as an extra care

# now we can compare
has_changed = wfs_source.compare()

with open('reports/wfs_updated.txt','w+') as handle:
    handle.write(f'{has_changed!s}')

if has_changed:
    print('changes in data have been DETECTED')
else:
    print('NO CHANGES in data have been detected')







