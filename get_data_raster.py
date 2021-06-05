# from owslib.util import dump
from study_case_config import *
from library import data_fetch as df

"""
 this script are intended to obtain data from the wfs datasource and then store memory-stored data into pickles, so one can check if there are updates on datasources, so all the process can be started over


# all the variables are from the file "study case "

modify it to another study-case

"""

#the pickler object to turn memory-stored objects into files
dumper = df.object_pickler()

# we will fetch data from the raster source (DEM)
dtm_raster_source = df.imagery_fetcher(dtm_link_list,extension=dtm_image_extension,imagery_name='DTM')

dsm_raster_source = df.imagery_fetcher(dsm_link_list,extension=dsm_image_extension,imagery_name='DSM')



# dumper.pickle_an_object(dtm_raster_source,dtm_pickle_filename)
# dumper.pickle_an_object(dsm_raster_source,dsm_pickle_filename)




