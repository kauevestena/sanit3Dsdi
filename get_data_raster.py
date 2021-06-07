# from owslib.util import dump
from study_case_config import *
from library import data_fetch as df
import os

"""
 this script are intended to obtain data from the wfs datasource and then store memory-stored data into pickles, so one can check if there are updates on datasources, so all the process can be started over


# all the variables are from the file "study case "

modify it to another study-case

"""

# we will fetch data from the raster source (DEM)
dtm_raster_source = df.imagery_fetcher(dtm_link_list,extension=dtm_image_extension,imagery_name='DTM')
dsm_raster_source = df.imagery_fetcher(dsm_link_list,extension=dsm_image_extension,imagery_name='DSM')

# getting bounding box for both:
dtm_bounding_box = dtm_raster_source.get_a_bounding_box(wfs_dump_filename,wgs84bboxkey)
dsm_bounding_box = dsm_raster_source.get_a_bounding_box(wfs_dump_filename,wgs84bboxkey)

#getting data, if bounding box are valid
if not dtm_bounding_box.is_empty:
    dtm_raster_source.retrieve_within_wgs84_bounds(dtm_bounding_box)

if not dsm_bounding_box.is_empty:
    dsm_raster_source.retrieve_within_wgs84_bounds(dsm_bounding_box)

# compile and dump infos for future checking:
dtm_raster_source.compile_and_dump_interest_infos()
dsm_raster_source.compile_and_dump_interest_infos()





