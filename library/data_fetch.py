# from platform import node
import datetime
from sys import excepthook
from numpy.lib.function_base import select
from owslib.wfs import WebFeatureService
import geopandas as gpd
from requests import Request as req
from shapely.geometry.polygon import Polygon
# from library import basic_functions as bf
import library.basic_functions as bf
from shapely.geometry import Polygon as sh_polygon
import json, os, time
from shapely import wkt

wgs84_code = "EPSG:4326"


class wfs_data_fetcher:

    connection = None # the WFS object
    wfs_url = ''
    municipalities = None # the municipalities geoDataFrame
    layer_hashes = {} # to store hashcode of interest layers
    layer_urls = {}
    layer_filepaths = {}
    layers = {'sanitation':{}} #to store interest_layers
    # to control if the interest infos have been compiled
    infos_compiled = False

    def __init__(self,wfs_url,json_dumpfile_name='wfs_data_dump.json',checking_mode=False):
        # the constructor

        while True:
            try:
                print('starting connection with ',wfs_url,'  ...')
                self.checking_mode = checking_mode
                self.connection = WebFeatureService(wfs_url)
                self.layer_list = list(self.connection.contents)
                self.dumpfile_name = json_dumpfile_name

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

        # dumping to .geojson
        outpath = os.path.join(bf.default_output_folder,layername+'.geojson')

        self.layer_filepaths[layername] = outpath

        if not self.checking_mode:

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

        self.interest_infos = {'layer_url':self.layer_urls,'layer_hash':self.layer_hashes,'layer_paths':self.layer_filepaths,'creation_date': str(datetime.date.today()),'hash_algorithm':bf.hash_algo}
        
        if not self.checking_mode:
            self.interest_infos['wgs84_bounding_box'] = self.wgs84_bbox.wkt

        self.json_outpath = os.path.join(bf.default_output_folder,self.dumpfile_name)
        self.infos_compiled = True

        if (not only_compile) or (not self.checking_mode):
            with open(self.json_outpath,'w+') as handle:
                json.dump(self.interest_infos,handle)
            print('file for future comparing created!!')
        else:
            print('infos not dumped, you probabily are checking for updates in wfs data!!')

    def compare(self):
        if not self.checking_mode:
            print('object not created in checking mode, look at the constructor call')
        else:
            has_changed = False

            if os.path.exists(self.json_outpath):
                with open(self.json_outpath) as opener:
                    input_dict = json.load(opener)
            else:
                print('file for comparation not avaliable')
                return None

            date_in = input_dict['creation_date']
            date_curr = self.interest_infos['creation_date']

            # now we can compare both
            reportname = f'reports/wfs_{date_in}_with_{date_curr}.txt'

            with open(reportname,'w+') as handle:
                if input_dict['hash_algorithm'] == self.interest_infos['hash_algorithm']:
                    if date_in == date_curr:
                        handle.write('files from same date!!!\n\n')
                    else:
                        handle.write(f'different dates, comparing from {date_in} with {date_curr}:\n\n')

                    # now we will compare layer hashes:
                    for layername in self.interest_infos['layer_hash']:
                        layerhash_curr = self.interest_infos['layer_hash'][layername]

                        try: #as an older dict can have different layers
                            layerhash_in = input_dict['layer_hash'][layername]

                            if layerhash_in == layerhash_curr:
                                handle.write(f'layer {layername} not changed. hashcode: {layerhash_in}\n')
                            else:
                                handle.write(f'layer {layername} HAS changed!! old hashcode: {layerhash_in}, new hashcode {layerhash_curr}\n')
                                has_changed = True # most important statement

                        except:
                            handle.write(f'layer {layername} not avaliable in the input file\n') 
                            continue
                else:
                    handle.write('different algorithms for hashing, impossible to compare!!')

                if has_changed:
                    handle.write('\nchanges in data have been detected!!')


            return has_changed
                
        

    


class imagery_fetcher:
    # a class to fetch imagery from a datasource

    checksums = {}
    downloaded_images = {}

    def __init__(self,source_url,stats_without_download=False,source_type = 'txt_list',extension='.tif',imagery_name='DEM',checking_mode=False,json_dumpfile_name='raster_data_dump.json',max_timeouts=10):

        # TODO : another datasources beyond text list
        self.checking_mode = checking_mode
        self.dumpfile_name = json_dumpfile_name


        if source_type == 'txt_list':
            # select only the entries that are actual images, not auxiliary files
            self.link_list = bf.select_entries_with_extension(bf.txt_from_url_to_list(source_url),extension)

            # remove that xml

            number_of_images = len(self.link_list)

            print('connecting with txt list from: ',source_url,' with ',number_of_images,' images')

            self.name = imagery_name
            self.missing_report_path = f'reports/failed_images{self.name}.txt'

            #getting boundingboxes from each image, storing in a geodatagrame

            wgs84_boundingboxes = {'url':[],'geometry':[]}

            self.missing_images = []

            self.tempfiles_outdir = os.path.join(bf.default_output_folder,'temp_images')

            bf.create_dir_ifnot_exists(self.tempfiles_outdir)

            
            for i,image_url in enumerate(self.link_list):
                t1 = time.time()

                print('opening',image_url)

                timeouts = 0

                sucess = True

                # tried_once = False 

                while True: # try considering timeout until sucess
                    try:

                        json_info = bf.parseGdalinfoJson(image_url,True,stats_without_download,outfolder_for_temporaries=self.tempfiles_outdir)
                
                        break
                    
                    except:
                        timeouts += 1
                        if timeouts > max_timeouts:
                            print('at ',i,' throwing the missing image to the end of image list ',image_url)
                            

                            self.missing_images.append(image_url)

                            # throwing the missing image to the end of image list
                            self.link_list.append(image_url)

                            if i > number_of_images:
                                with open(self.missing_report_path,'a+') as handle:
                                    handle.write(image_url+'at '+str(i)+'\n')

                            sucess = False
                            break 
                        else:
                            print('timeout reached, trying again')


                if sucess:
                    wgs84_boundingboxes['url'].append(image_url)

                    wgs84_boundingboxes['geometry'].append(sh_polygon(json_info['wgs84Extent']['coordinates'][0]))

                    #the image checksum

                    sum = 0
                    for band in json_info['bands']:
                        sum += int(band['checksum'])
                    
                    self.checksums[image_url] = sum

                bf.print_rem_time_info(len(self.link_list)-1,i,t1)


            self.imagery_bboxes_wgs84 = gpd.GeoDataFrame(wgs84_boundingboxes,crs=wgs84_code)

            self.bbox_outpath = os.path.join(bf.default_output_folder,'bounding_boxes_wgs84_'+self.name+'.geojson')

            self.imagery_bboxes_wgs84.to_file(self.bbox_outpath,driver='GeoJSON')


            print('bounding boxes recorded!!')

            # deleting temporary folder as its generally leaves garbage in
            time.sleep(1)
            bf.delete_folder_if_exists(self.tempfiles_outdir)


        #else if:
        #  another possibilities

    def get_a_bounding_box(self,filename,inputkey=None,filetype='json'):

        filepath = os.path.join(bf.default_output_folder,filename)

        if filetype == 'json':
            with open(filepath) as handle:
                input_dict = json.load(handle)

            print('retrieved a bounding box!')


            return wkt.loads(input_dict[inputkey])

            
        
        else:
            print('currently only supports .json file as input')

            return Polygon()


    def retrieve_within_wgs84_bounds(self,boundaries):
        '''
            retrieve only the features within the interest area, 
            
            boundaries must be a shapely polygon or another GeoDataFrame/GeoSeries (intended to be connected with a 
            
            wfs_data_fetcher.clipping_polygon_wgs84 

            to download only interest imagery
        '''
     
        # imagery whose bounding boxes intersects interest areas    
        intersect_entries = self.imagery_bboxes_wgs84.intersects(boundaries)

        self.interest_entries =  self.imagery_bboxes_wgs84[intersect_entries]

        # finally we will download the imagery
        for image_url in self.interest_entries["url"]:
            print('donwloading ',image_url)

            while True:
                try:
                    print()
                    img_outpath = bf.download_file_from_url(image_url,return_filename=False,timeout=True)
                    self.downloaded_images[image_url] = img_outpath
                    break
                except:
                    print('timeout reached, trying again')



    def compile_and_dump_interest_infos(self,only_compile=False): #FOR RASTER DATA, DO NOT CONFUSE WITH WFS COUNTERPART
        self.interest_infos = {'checksums':self.checksums,'creation_date':str(datetime.date.today()),'bounding_boxes_path':self.bbox_outpath,'downloaded_image_path':self.downloaded_images}

        self.json_outpath = os.path.join(bf.default_output_folder,self.dumpfile_name)

        if (not only_compile) or (not self.checking_mode):
            with open(self.json_outpath,'w+') as handle:
                json.dump(self.interest_infos,handle)
            print('file for future comparing created!!')

        else:
            print(f'infos not dumped, you probabily are checking for updates in raster data!!')


    def compare(self):
        if not self.checking_mode:
            print('object not created in checking mode, look at the constructor call')
        else:
            has_changed = False

            if os.path.exists(self.json_outpath):
                with open(self.json_outpath) as opener:
                    input_dict = json.load(opener)
            else:
                print('file for comparation not avaliable')
                return None

            date_in = input_dict['creation_date']
            date_curr = self.interest_infos['creation_date']

            # now we can compare both
            reportname = f'reports/{self.name}_raster_{date_in}_with_{date_curr}.txt'

            with open(reportname,'w+') as handle:
                if date_in == date_curr:
                    handle.write('files from same date!!!\n\n')
                else:
                    handle.write(f'different dates, comparing from {date_in} with {date_curr}:\n\n')

                # now we will compare layer hashes:
                for img_url in self.interest_infos['checksums']:
                    checksum_curr = self.interest_infos['checksums'][img_url]

                    try: #as an older dict can have different layers
                        checksum_in = input_dict['checksums'][img_url]

                        if checksum_in == checksum_curr:
                            handle.write(f'raster {img_url} not changed. checksum: {checksum_in}\n')
                        else:
                            handle.write(f'raster {img_url} HAS changed!! old checksum: {checksum_in}, new checksum {checksum_curr}\n')
                            has_changed = True # most important statement

                    except:
                        handle.write(f'raster {img_url} not avaliable in the input file\n') 
                        continue

                if has_changed:
                    handle.write('\nchanges in data have been detected!!')


            return has_changed




class osm_fetcher:

    # Constants that must be added to feature id in order to characterize areas in OSM
    # Generally a municipality is characterized as a relation (and most boundaries are as well)
    way_constant = 2400000000
    relation_constant = 3600000000

    layers = {}

    def __init__(self,interest_feature,added_constant=False,is_relation = True,bounging_box=None):

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
        print('getting buildings data, first the request:')
        query_string = bf.osm_query_string_by_id(self.interest_feature,node=False)

        self.layers['buildings'] = bf.get_osm_data(query_string,'buildings')

    def get_roads(self):
        print('getting road data, first the request:')

        query_string = bf.osm_query_string_by_id(self.interest_feature,'highway',node=False)

        self.layers['roads'] = bf.get_osm_data(query_string,'highways',interest_geom_type='LineString')

    def get_custom_tag(self,custom_tag,layername,getnodes=True,getways=True,getrelations=True):

        print('getting osm data, first the request:')

        query_string = bf.osm_query_string_by_id(self.interest_feature,custom_tag,node=getnodes,way=getways,relation=getrelations)

        self.layers[layername] = bf.get_osm_data(query_string,layername)




class object_pickler:
    '''
        DEPRECATED, WE ARE PREFERRING TO USE .json FILES
    '''


    # using encapsulation to get away from circular importing

    def __int__(self):
        print('pickler created!!')

    def pickle_an_object(self,input_object,filename):
        bf.object_pickling(input_object,filename)