from study_case_config import *
from library import data_fetch as df

"""
 this script are intended to obtain data from the datasources and then store memory-stored data into pickles, so one can check if there are updates on datasources, so all the process can be started over


# all the variables are from the file "study case "

modify it to another study-case

"""


# first we will fetch data from the wfs source (pipery)
wfs_source = df.wfs_data_fetcher(wfs_url)

# acquiring the boundary layer
wfs_source.get_municipalities(mun_lyr_name,[IBGE_code_municipality],mun_id_field,alt_field=alt_field,alt_value=alt_value)

# acquiring (also downloading as geojson) the interest layers, default are layers from sanitation
wfs_source.get_interest_list_of_layers(interest_layers_keystring)

#dumping interest data, including paths for download layers
wfs_source.compile_and_dump_interest_infos()




