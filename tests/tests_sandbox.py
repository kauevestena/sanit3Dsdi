
import wget

sample_url = "https://geobases.static.es.gov.br/public/MAP_ES_2012_2015/MDE/39_781.img"


wget.download(sample_url,'sample_img.img')