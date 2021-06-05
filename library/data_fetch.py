# from platform import node
# import time
from sys import excepthook
from owslib.wfs import WebFeatureService
import geopandas as gpd
from requests import Request as req
# from library import basic_functions as bf
import library.basic_functions as bf
from shapely.geometry import Polygon as sh_polygon
import json, os


wgs84_code = "EPSG:4326"


class wfs_data_fetcher:

    connection = None # the WFS object
    wfs_url = ''
    municipalities = None # the municipalities geoDataFrame
    layer_hashes = {} # to store hashcode of interest layers
    layer_urls = {}
    layer_filepaths = {}
    layers = {'sanitation':{}} #to store interest_layers

    def __init__(self,wfs_url):
        # the constructor

        while True:
            try:
                print('starting connection with ',wfs_url,'  ...')
                self.connection = WebFeatureService(wfs_url)
                self.layer_list = list(self.connection.contents)

                if self.layer_list: #check by its contents that the connection suceeded
                    print('connection sucessful!!')
                    break
            except:
                print('connection not sucessful, retrying')
        self.wfs_url = wfs_url


    def layer_to_gdf(self,layername,print_req_url=True):
        '''
            transform a vector layer in the wfs datasource to a GeoDataFrame 
        '''

        # TODO ALSO DUMP TO GEOJSON FILE

        # parameters to create url_request:
        params = dict(service='WFS', version="1.0.0", request='GetFeature',typeName=layername,outputFormat='json')
        req_url = req('GET', self.wfs_url, params=params).prepare().url

        if print_req_url:
            print(req_url)

        #record the hash from the data as the hash from json as string:
        self.layer_hashes[layername] = bf.get_hash_from_text_in_url(req_url)
        # recording the request url:
        self.layer_urls[layername] = req_url

        as_gdf = gpd.read_file(req_url)

        outpath = os.path.join(bf.default_output_folder,layername+'.geojson')

        self.layer_filepaths[layername] = outpath

        as_gdf.to_file(outpath,driver='GeoJSON')

        return as_gdf


    def get_municipalities(self,municipalities_layername,subset_ibge_codes=[],ibge_cod_field='cod_ibge',alt_field=None,alt_value=None,print_mun_gdf_head=False):
        '''
            
        '''
        if municipalities_layername in self.layer_list:
            #select the layer containing the municipalities, a special layer, since it will be used as the cropping (clip) layer
            if not subset_ibge_codes:
                self.municipalities = self.layer_to_gdf(municipalities_layername)
            else:
                mun_gdf = self.layer_to_gdf(municipalities_layername)
                if print_mun_gdf_head:
                    print(mun_gdf.head())
                self.municipalities = mun_gdf.loc[mun_gdf[ibge_cod_field].isin(subset_ibge_codes)]
                if self.municipalities.empty:
                    print(ibge_cod_field,subset_ibge_codes)
                    try:
                        # sometimes a string representation does not work
                        self.municipalities = mun_gdf.loc[mun_gdf[int(ibge_cod_field)].isin(subset_ibge_codes)]
                    except:
                        print('trying by alternate fields!')
                        try:
                            self.municipalities = mun_gdf.loc[mun_gdf[alt_field].isin([alt_value])]

                        except:
                            print('trouble or alternate values not established')


            print(self.municipalities.head())

            # obtaining the bounding box of the interest area

            self.wgs84_bbox = bf.geodataframe_bounding_box(self.municipalities)

            self.clipping_polygon = self.municipalities.dissolve()

            self.clipping_polygon_wgs84 = self.clipping_polygon.to_crs(wgs84_code)
        else:
            print('layer name not found in database!!')


    def get_layerlist(self):

        return list(self.connection.contents)

    def dump_layerlist(self,outpath):
        bf.list_dump(self.layer_list, outpath)

    def get_interest_list_of_layers(self,selection_keystring,category_key='sanitation',print_columns=True):

        #selecting interest layers from layerlist
        layername_list = bf.select_entries_with_string(self.layer_list,selection_keystring)

        curr_dict = self.layers[category_key]

        for layername in layername_list:
            curr_dict[layername] = self.layer_to_gdf(layername)
            print('imported layer ',layername)
            if(print_columns):
                print(curr_dict[layername].columns)
        # funtion used to store all of the interest layers in dictionary

    def compile_and_dump_interest_infos(self,only_compile=False):
        self.interest_infos = {'layer_url':self.layer_urls,'layer_hash':self.layer_hashes,'layer_paths':self.layer_filepaths,'wgs84_bounding_box':self.wgs84_bbox}

        if not only_compile:
            pass

class imagery_fetcher:
    # a class to fetch imagery from a datasource

    checksums = {}

    def __init__(self,source_url,source_type = 'txt_list',extension='.tif',imagery_name='DEM'):

        # TODO : another datasources beyond text list

        if source_type == 'txt_list':
            # select only the entries that are actual images, not auxiliary files
            self.link_list = bf.select_entries_with_string(bf.txt_from_url_to_list(source_url),extension)

            self.name = imagery_name

            #getting boundingboxes from each image, storing in a geodatagrame

            wgs84_boundingboxes = {'url':[],'geometry':[]}

            for image_url in self.link_list:
                json_info = bf.parseGdalinfoJson(image_url)


                wgs84_boundingboxes['url'].append(image_url)

                wgs84_boundingboxes['geometry'].append(sh_polygon(json_info['wgs84Extent']['coordinates'][0]))

                #the image checksum

                sum = 0
                for band in json_info['bands']:
                    sum += int(band['checksum'])
                
                self.checksums[image_url] = sum


            self.imagery_bboxes_wgs84 = gpd.GeoDataFrame(wgs84_boundingboxes,crs=wgs84_code)


        #else if:
        #  another possibilities

    def retrieve_within_wgs84_bounds(self,boundaries):
        '''
            retrieve only the features within the interest area, 
            
            boundaries must be a shapely polygon or another GeoDataFrame/GeoSeries (intended to be connected with a 
            
            wfs_data_fetcher.clipping_polygon_wgs84 

            to download only interest imagery
        '''
     
        # imagery whose bounding boxes intersects interest areas    
        intersect_entries = self.imagery_bboxes_wgs84.intersects[boundaries]

        self.interest_entries =  self.imagery_bboxes_wgs84[intersect_entries]

        # finally we will download the imagery
        for image_url in self.interest_entries["url"]:
            bf.download_file_from_url(image_url)


class osm_fetcher:

    # Constants that must be added to feature id in order to characterize areas in OSM
    # Generally a municipality is characterized as a relation (and most boundaries are as well)
    way_constant = 2400000000
    relation_constant = 3600000000

    layers = {}

    def __init__(self,interest_feature=0,added_constant=False,is_relation = True,bounging_box=None):

        if interest_feature == 0:
            # TODO make an implementation for a wgs84 bounding box
            pass
        else:
            if added_constant:
                self.interest_feature = interest_feature
            else:
                if is_relation:
                    self.interest_feature = int(interest_feature) + self.relation_constant
                else:
                    self.interest_feature = int(interest_feature) + self.way_constant

    # to get data use methods below:
    def get_buildings(self):
        query_string = bf.osm_query_string_by_id(self.interest_feature,node=False)

        self.layers['buildings'] = bf.get_osm_data(query_string,'buildings')

    def get_roads(self):
        query_string = bf.osm_query_string_by_id(self.interest_feature,'highway',node=False)

        self.layers['roads'] = bf.get_osm_data(query_string,'highways')

    def get_custom_tag(self,custom_tag,layername,getnodes=True,getways=True,getrelations=True):

        query_string = bf.osm_query_string_by_id(self.interest_feature,custom_tag,node=getnodes,way=getways,relation=getrelations)

        self.layers[layername] = bf.get_osm_data(query_string,layername)


class object_pickler:
    # using encapsulation to get away from circular importing

    def __int__(self):
        print('pickler created!!')

    def pickle_an_object(self,input_object,filename):
        bf.object_pickling(input_object,filename)