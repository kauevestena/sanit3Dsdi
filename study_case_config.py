


"""
    this file is intended to set-up the study-case
    the original study case are from the municipality of Vitoria-ES (BR)
"""



# url for the Vector data, in study-case it is from Geobases
wfs_url = "https://ide.geobases.es.gov.br/geoserver/geonode/wfs"

# link list for dtm (ground-level) and dsm (highest at "plane" point)
dtm_link_list = "https://geobases.static.es.gov.br/public/MAP_ES_2012_2015/MAP_ES_2012_2015_MDT_URL_LIST.txt"

dtm_image_extension = '.img'

dsm_link_list = "https://geobases.static.es.gov.br/public/MAP_ES_2012_2015/MAP_ES_2012_2015_MDE_URL_LIST.txt"

dsm_image_extension = '.img'


# we tried to import from an A3 Minio database, without sucess


# the boundary relation to fetch osm data,
#  in the study case is from the municipality of Vitoria-ES (BR)
osm_boundary_id = 1825817

# municipalityes layer name:
mun_lyr_name = 'geonode:idaf_limite_municipal_2018_11' 


# IBGE code for the municipality 'Vitória'
IBGE_code_municipality = '3205309'

# field for municipality identification
mun_id_field = 'cod_ibge'

# alternate way to try to obtain municipality polygon:
alt_field = 'nome'
alt_value = 'Vitória'

# keystring to select interest layers
interest_layers_keystring = 'cesan'


# the default filename for pickled objects, you can leave as the default filenames 
wfs_pickle_filename = 'wfs_source.pickle'
dtm_pickle_filename = 'dtm_source.pickle'
dsm_pickle_filename = 'dsm_source.pickle'
osm_pickle_filename = 'osm_source.pickle'