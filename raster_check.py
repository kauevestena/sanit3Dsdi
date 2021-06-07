# from owslib.util import dump
from study_case_config import *
from library import data_fetch as df
import os

"""
 this script are intended to check if raster datasource have been updated

"""

# we will fetch data from the raster source (DEM)
dtm_raster_source = df.imagery_fetcher(dtm_link_list,extension=dtm_image_extension,imagery_name='DTM',checking_mode=True)
dsm_raster_source = df.imagery_fetcher(dsm_link_list,extension=dsm_image_extension,imagery_name='DSM',checking_mode=True)

# compile and dump infos for future checking:
dtm_raster_source.compile_and_dump_interest_infos()
dsm_raster_source.compile_and_dump_interest_infos()



#now we can check infos:

dtm_has_changed = dtm_raster_source.compare()

with open('reports/dtm_updated.txt','w+') as handle:
    handle.write(f'{dtm_has_changed!s}')

if dtm_has_changed:
    print('changes in dtm data have been DETECTED')
else:
    print('NO CHANGES in dtm data have been detected')



dsm_has_changed = dsm_raster_source.compare()

with open('reports/dsm_updated.txt','w+') as handle:
    handle.write(f'{dsm_has_changed!s}')

if dsm_has_changed:
    print('changes in dsm data have been DETECTED')
else:
    print('NO CHANGES in dsm data have been detected')




