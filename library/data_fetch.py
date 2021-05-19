import time
from owslib.wfs import WebFeatureService
import geopandas as gpd
from requests import Request as req
from library import basic_functions as bf


class wfs_data_fetcher:

    connection = None # the WFS object
    wfs_url = ''
    municipalities = None # the municipalities geoDataFrame
    layer_hashes = {} # to store hashcode of interest layers
    layers = {'sanitation':{}} #to store interest_layers

    def __init__(self,wfs_url):
        # the constructor
        self.connection = WebFeatureService(wfs_url)
        self.wfs_url = wfs_url
        self.layer_list = list(self.connection.contents)


    def layer_to_gdf(self,layername):


        # parameters to create url_request:
        params = dict(service='WFS', version="1.0.0", request='GetFeature',typeName=layername,outputFormat='json')
        req_url = req('GET', self.wfs_url, params=params).prepare().url

        #record the hash from the data:
        self.layer_hashes[layername] = bf.get_hash_from_text_in_url(req_url)

        return gpd.read_file(req_url)


    def get_municipalities(self,municipalities_layername,subset_ibge_codes=[],ibge_cod_field='cod_ibge'):

        #select the layer containing the municipalities, a special layer, since it will be used as the cropping (clip) layer
        if not subset_ibge_codes:
            self.municipalities = self.layer_to_gdf(municipalities_layername)
        else:
            mun_gdf = self.layer_to_gdf(municipalities_layername)
            self.municipalities = mun_gdf.loc[mun_gdf[ibge_cod_field].isin(subset_ibge_codes)]


        # obtaining the bounding box of the interest area

        self.wgs84_bbox = bf.geodataframe_bounding_box(self.municipalities)

        self.clipping_polygon = self.municipalities.dissolve()


    def get_layerlist(self):

        return list(self.connection.contents)

    def dump_layerlist(self,outpath):
        bf.list_dump(self.layer_list, outpath)

    def get_interest_layer_list(self,selection_keystring,category_key):

        #selecting interest layers from layerlist
        layername_list = bf.select_entries_with_string(self.layer_list,selection_keystring)

        curr_dict = layers[category_key]

        for layername in layername_list:
            curr_dict[layername] = self.layer_to_gdf(layername)
        # funtion used to store all of the interest layers in dictionary


class imagery_fetcher:
    # a class to fetch imagery from a datasource

    def __init__(self,source_url,source_type = 'txt_list',extension='.tif',imagery_name=''):

        if source_type == 'txt_list':
            self.link_list = bf.select_entries_with_string(bf.txt_from_url_to_list(source_url),extension)

            self.name = imagery_name

    def retrieve_within_wgs84_bounds(self,boundaries):
        pass