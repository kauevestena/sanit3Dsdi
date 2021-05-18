#!/bin/bash

cd tests

gdalinfo /vsicurl/https://geobases.static.es.gov.br/public/MAP_ES_2012_2015/MDE/38_790.img -json > test_gdalinfo_out.json

gdalinfo /vsicurl/https://geobases.static.es.gov.br/public/MAP_ES_2012_2015/MDE/38_790.img > test_gdalinfo_out.txt