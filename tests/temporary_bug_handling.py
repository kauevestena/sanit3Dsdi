import library.basic_functions as bf
import json


jsonpath = '/home/kaue/data/sanit3d_out/temporary/dtm_raster_data_dump.json'


with open(jsonpath) as reader:
    input_dict = json.load(reader)

for imgurl in input_dict['downloaded_image_path']:
    print('downloading from ',imgurl)
    bf.download_file_from_url(imgurl,timeout=True,filename_preffix='DTM_',try_till_download=True)

print('total ',len(input_dict['downloaded_image_path']),' images')