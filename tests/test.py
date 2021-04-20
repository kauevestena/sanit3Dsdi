import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import time
start_time = time.time()

from bib import constants
from owslib.wfs import WebFeatureService

#geobases wfs url
gb_wfs = constants.geobases_wfs_url


geobases = WebFeatureService(gb_wfs)

# name
print(geobases.identification.title)
# operations
print([operation.name for operation in geobases.operations])
#contents
print(geobases.contents)

print("--- %s seconds ---" % (time.time() - start_time))
# # # from PyInstaller.utils.hooks import collect_data_files
# # # datas = collect_data_files('pyproj')