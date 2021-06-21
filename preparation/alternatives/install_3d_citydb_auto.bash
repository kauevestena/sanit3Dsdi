#!/bin/bash

# dependencies
# 1: postgis

# POSTGRE
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql

#POSTGIS
sudo apt install postgis

# 2: JDK
sudo apt install default-jdk


# GET THE LATEST 3DCITYDB RELEASE
# TODO: give a way to obtain automatically hte latest
wget https://github.com/3dcitydb/importer-exporter/releases/download/v4.3.0/3DCityDB-Importer-Exporter-4.3.0-Setup.jar

# launching the graphical interface installer:
# help through installation can be found here:
# https://3dcitydb-docs.readthedocs.io/en/latest/first-steps/install-impexp.html
java -jar 3DCityDB-Importer-Exporter-4.3.0-Setup.jar preparation/alternatives/3d-citydb_instscript.xml