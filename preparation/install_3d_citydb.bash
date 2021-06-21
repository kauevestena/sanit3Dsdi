#!/bin/bash

# dependencies
# 1: postgis

# following https://www.vultr.com/docs/install-the-postgis-extension-for-postgresql-on-ubuntu-linux
# POSTGRE
sudo apt -y install gnupg2
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
sudo apt -y install postgresql-12 postgresql-client-12
sudo apt install postgis postgresql-12-postgis-3
sudo apt-get install postgresql-12-postgis-3-scripts

# 2: JDK
sudo apt install default-jdk


# GET THE LATEST 3DCITYDB RELEASE
# TODO: give a way to obtain automatically hte latest
wget https://github.com/3dcitydb/importer-exporter/releases/download/v4.3.0/3DCityDB-Importer-Exporter-4.3.0-Setup.jar

# launching the graphical interface installer:
# help through installation can be found here:
# https://3dcitydb-docs.readthedocs.io/en/latest/first-steps/install-impexp.html
# TODO (maybe as we are running one-time installer): full-command-line installation
java -jar 3DCityDB-Importer-Exporter-4.3.0-Setup.jar