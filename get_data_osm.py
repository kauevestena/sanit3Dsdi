# from owslib.util import dump
from study_case_config import *
from library import data_fetch as df
import os

"""
 this script are intended to obtain data from the OSN datasource and then store memory-stored data  so one can check if there are updates on datasources, so all the process can be started over


# all the variables are from the file "study case "

modify it to another study-case

"""

# we will fetch data from OSM
osm_data_fetch = df.osm_fetcher(osm_boundary_id)

osm_data_fetch.get_buildings()

osm_data_fetch.get_roads()


# we have not implemented checking in OSM data since it is always changing

