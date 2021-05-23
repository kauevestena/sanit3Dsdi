import time
from owslib.wfs import WebFeatureService
import geopandas as gpd
from requests import Request as req
from library import basic_functions as bf
from shapely.geometry import Polygon as sh_polygon


wgs84_code = "EPSG:4326"


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
        '''
            transform a vector layer in the wfs datasource to a GeoDataFrame 
        '''


        # parameters to create url_request:
        params = dict(service='WFS', version="1.0.0", request='GetFeature',typeName=layername,outputFormat='json')
        req_url = req('GET', self.wfs_url, params=params).prepare().url

        #record the hash from the data:
        self.layer_hashes[layername] = bf.get_hash_from_text_in_url(req_url)

        return gpd.read_file(req_url)


    def get_municipalities(self,municipalities_layername,subset_ibge_codes=[],ibge_cod_field='cod_ibge'):
        '''
            
        '''

        #select the layer containing the municipalities, a special layer, since it will be used as the cropping (clip) layer
        if not subset_ibge_codes:
            self.municipalities = self.layer_to_gdf(municipalities_layername)
        else:
            mun_gdf = self.layer_to_gdf(municipalities_layername)
            self.municipalities = mun_gdf.loc[mun_gdf[ibge_cod_field].isin(subset_ibge_codes)]


        # obtaining the bounding box of the interest area

        self.wgs84_bbox = bf.geodataframe_bounding_box(self.municipalities)

        self.clipping_polygon = self.municipalities.dissolve()

        self.clipping_polygon_wgs84 = self.clipping_polygon.to_crs(wgs84_code)


    def get_layerlist(self):

        return list(self.connection.contents)

    def dump_layerlist(self,outpath):
        bf.list_dump(self.layer_list, outpath)

    def get_interest_layer_list(self,selection_keystring,category_key):

        #selecting interest layers from layerlist
        layername_list = bf.select_entries_with_string(self.layer_list,selection_keystring)

        curr_dict = self.layers[category_key]

        for layername in layername_list:
            curr_dict[layername] = self.layer_to_gdf(layername)
        # funtion used to store all of the interest layers in dictionary


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


