# warning supŕession 
# import re
# from tempfile import TemporaryDirectory
import shutil
from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)

import os, requests, hashlib, subprocess, json, pickle, time
import geopandas as gpd
from shapely.geometry import box as sh_box
from urllib.parse import urlparse
from wget import download as wget_download
import library.constants as constants
from timeout_decorator import timeout #just ignore if pylance complains

default_timeout = 30

def joinToHome(input_path):
    """
    join a relative path to the home path
    """
    return os.path.join(os.environ['HOME'],input_path.strip('/'))

def create_dir_ifnot_exists(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def createDirs(dirList):
    for dirPath in dirList:
        create_dir_ifnot_exists(dirPath)

def list_dump(input_list,outpath,mode='w+'):
    with open(outpath,mode) as list_writer:
        for item in input_list:
            list_writer.write(str(item)+'\n')

def get_hash_from_text_in_url(url):
    textstring = requests.get(url).text
    return hash_string(textstring)

hash_algo = 'sha256'

def hash_string(inputstr,algorithm=hash_algo):
    # TODO save hash encoding
    hasher = hashlib.new(algorithm)
    hasher.update(inputstr.encode())
    return hasher.hexdigest()

def select_entries_with_string(inputlist,inputstring):
    return [entry for entry in inputlist if inputstring in entry]

def select_entries_with_extension(inputlist,ext_string):
    # this one will prevent from things like "archive.desired_ext.other_ext"
    out_list = []
    for entry in inputlist:
        if entry.endswith(ext_string):
            out_list.append(entry)

    return out_list

def delete_folder_if_exists(folderpath):
    if os.path.exists(folderpath):
        shutil.rmtree(folderpath)

# TODO IMPROVE TIMEOUT
# but that is tricky as depends on internet speed
@timeout(default_timeout)
def  parseGdalinfoJson(inputpath,print_runstring=False,from_www=True,local_file=False,optionals = '',print_outstring=False,outfolder_for_temporaries=None):
    '''
        Parse GDALINFO from a OGR compliant image as json. The image can be web-hosted or no.
    '''

    url_preffix = ''

    if from_www:
        url_preffix = '/vsicurl/'
    else:
        if not local_file: # so one can give a path from a local file
            if outfolder_for_temporaries:
                inputpath = download_file_from_url(inputpath,return_filename=False,outfolder = outfolder_for_temporaries)
            else:
                inputpath = download_file_from_url(inputpath,return_filename=False)
            print() # just to break a line 

    # if quoted_path:
    #     inputpath = '"'+inputpath+'"'

    runstring = f'gdalinfo "{url_preffix}{inputpath}" -json -stats -checksum {optionals}'

    if print_runstring:
        print(runstring)
    
    # the magic part from some handsome person from stack overflow
    out = subprocess.run(runstring,shell=True,stdout=subprocess.PIPE)

    as_str = out.stdout.decode('utf-8').replace('\\n','')
    #####

    if print_outstring:
        print(as_str)

    # cleaning up in case of donwload temporary
    if (not from_www) and (not local_file):
        time.sleep(1)
        delete_filelist_that_exists([inputpath])
        if not os.path.exists(inputpath):
            print('file ',inputpath,' deleted!!!')

    return json.loads(as_str)


def txt_from_url_to_list(input_url):
    '''
    obtaining a list of lines from a url
    '''
    return requests.get(input_url).text.splitlines()


def geodataframe_bounding_box(input_gdf,as_wgs84=True):
    '''
        Bounding box from a geodataframe as a shapely polygon. DEFAULT AS WGS84
    '''

    if as_wgs84:
        # the '*' operator is required as shapely box asks for individual coordinates
        return sh_box(*input_gdf.to_crs("EPSG:4326").total_bounds)

    else:
        # to use native CRS
        return sh_box(*input_gdf.total_bounds)



def download_file_from_url(input_url,outfolder=constants.temp_files_outdir,return_filename=True,timeout=False,filename_preffix=None,try_till_download=False):
    '''
        download a file specifying some conditions, the "try_till_download" parameter will override 'timeout' parameter
    '''
    #thx: https://stackoverflow.com/a/18727481/4436950
    #thx: https://is.gd/FkH1td 
    
    # the url as a path
    url_path = urlparse(input_url).path

    
    filename = os.path.basename(url_path)

    if filename_preffix:
        filename = filename_preffix + filename

    outpath = os.path.join(outfolder,filename)

    #with the tailored outpath, we can download the file
    
    if not try_till_download:
        if timeout:
            wget_download_with_timeout(input_url,outpath)
        else:
            wget_download(input_url,outpath)
    else:
        while True:
            try:
                print()
                wget_download_with_timeout(input_url,outpath)
                print()
                time.sleep(1)
                break
            except:
                print('\ntimeout reached, trying again!!')


    if return_filename:
        return filename
    else:
        return outpath


@timeout(default_timeout)
def wget_download_with_timeout(input_url,outpath):
    wget_download(input_url,outpath)





def object_pickling(input_object,filename,outfolder=constants.temp_files_outdir,pickle_protocol=4):
    '''
        to store dataFetching classes, mostly for check for updates in remote datasources
    '''

    outpath = os.path.join(outfolder,filename)

    with open(outpath,'wb') as handle:
        pickle.dump(input_object,handle,protocol=pickle_protocol)
    

def osm_query_string_by_id(interest_area_code,interest_tag="building",node=True,way=True,relation=True,print_querystring=False):
    '''
        generates a specific query string for overpass API
    '''

    node_part = way_part = relation_part = ''

    if node:
        node_part = f'node["{interest_tag}"](area:{interest_area_code});'
    if way:
        way_part = f'way["{interest_tag}"](area:{interest_area_code});'
    if relation:
        relation_part = f'relation["{interest_tag}"](area:{interest_area_code});'

    overpass_query = f"""
    (  
        {node_part}
        {way_part}
        {relation_part}
    );
    /*added by auto repair*/
    (._;>;);
    /*end of auto repair*/
    out;
    """

    if print_querystring:
        print(overpass_query)

    return overpass_query

def join_to_default_outfolder(filename,outfolder=constants.temp_files_outdir):

    return os.path.join(outfolder,filename)

def delete_filelist_that_exists(filepathlist):
    for filepath in filepathlist:
        if os.path.exists(filepath):
            os.remove(filepath)


def get_osm_data(querystring,tempfilesname,print_response=True,delete_temp_files=False,interest_geom_type='Polygon'):
    '''
        get the osmdata and stores in a geodataframe, also generates temporary files
    '''

    # the requests part:
    overpass_url = "http://overpass-api.de/api/interpreter" # there are also other options
    response = requests.get(overpass_url,params={'data':querystring})

    # TODO check the response, beyond terminal printing
    if print_response:
        print(response)

    # the outpaths for temporary files
    xmlfilepath = join_to_default_outfolder(tempfilesname+'_osm.xml')
    geojsonfilepath = join_to_default_outfolder(tempfilesname+'_osm.geojson')

    print('xml will be written to: ',xmlfilepath)

    # the xml file writing part:
    with open(xmlfilepath,'w+') as handle:
        handle.write(response.text)

    print('geojson will be written to: ',geojsonfilepath)

    # the command-line call
    runstring = f'osmtogeojson "{xmlfilepath}" > "{geojsonfilepath}"'

    out = subprocess.run(runstring,shell=True)

    print('conversion sucessfull!!')
    # reading as a geodataframe
    as_gdf = gpd.read_file(geojsonfilepath)

    # cleaning up, if wanted
    if delete_temp_files:
        delete_filelist_that_exists([xmlfilepath,geojsonfilepath])

    # return only polygons, we have no interest on broken features
    if interest_geom_type:
        new_gdf = as_gdf[as_gdf['geometry'].geom_type == interest_geom_type]

        #overwrite file with only selected features

        print('saving subset with only ',interest_geom_type)
        new_gdf.to_file(geojsonfilepath,driver='GeoJSON')

        return new_gdf
    else:
        return as_gdf

def print_rem_time_info(total_it,curent_it,ref_time):
    # "it" stands for 'iteration'
    it_time  = time.time()-ref_time
    rem_its  = total_it-curent_it
    rem_time = it_time * rem_its
    print("took {:.4f} seconds, estimated remaining time: {:.4f} minutes or {:.4f} hours, iteration {} of {}".format(it_time,rem_time/60.0,rem_time/3600.0,curent_it,total_it))

# aliasing to avoid circular importing
default_output_folder = constants.temp_files_outdir