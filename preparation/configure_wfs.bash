#!/bin/bash


# https://www.digitalocean.com/community/tutorials/install-tomcat-9-ubuntu-1804-pt
sudo groupadd tomcat

sudo useradd -s /bin/false -g tomcat -d /opt/tomcat tomcat

mkdir tomcat

cd tomcat

curl -O https://mirror.nbtelecom.com.br/apache/tomcat/tomcat-9/v9.0.48/bin/apache-tomcat-9.0.48.tar.gz

# admin123
# admin123


http://localhost:8080/citydb-wfs/wfs