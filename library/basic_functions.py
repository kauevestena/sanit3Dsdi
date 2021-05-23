# warning supŕession 
from tempfile import TemporaryDirectory
from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)

import os, requests, hashlib, subprocess, json, pickle
import geopandas as gpd
from shapely.geometry import box as sh_box
from urllib.parse import urlparse
from wget import download as wget_download
from library.constants import temp_files_outdir

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


def hash_string(inputstr):
    hasher = hashlib.sha256()
    hasher.update(inputstr.encode())
    return hasher.hexdigest()

def select_entries_with_string(inputlist,inputstring):
    return [entry for entry in inputlist if inputstring in entry]


def  parseGdalinfoJson(inputpath,print_runstring=False,from_www=True,optionals = '',print_outstring=False):
    '''
        Parse GDALINFO from a OGR compliant image as json. The image can be web-hosted or no.
    '''

    url_preffix = ''

    if from_www:
        url_preffix = '/vsicurl/'

    # if quoted_path:
    #     inputpath = '"'+inputpath+'"'

    runstring = f'gdalinfo "{url_preffix}{inputpath}" -json -stats -checksum {optionals}'

    if print_runstring:
        print(runstring)
    
    out = subprocess.run(runstring,shell=True,stdout=subprocess.PIPE)

    as_str = out.stdout.decode('utf-8').replace('\\n','')

    if print_outstring:
        print(as_str)

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



def download_file_from_url(input_url,outfolder=temp_files_outdir):
    #thx: https://stackoverflow.com/a/18727481/4436950
    #thx: https://is.gd/FkH1td 
    
    # the url as a path
    url_path = urlparse(input_url).path

    filename = os.path.basename(url_path)

    outpath = os.path.join(outfolder,filename)

    #with the tailored outpath, we can download the file
    wget_download(input_url,outpath)

    return filename

def object_pickling(input_object,filename,outfolder=temp_files_outdir,pickle_protocol=4):
    '''
        to store dataFetching classes, mostly for check for updates in remote datasources
    '''

    outpath = os.path.join(outfolder,filename)

    with open(outpath,'wb') as handle:
        pickle.dump(input_object,handle,protocol=pickle_protocol)
    