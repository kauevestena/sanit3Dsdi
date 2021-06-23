#!/bin/bash

# https://3dcitydb-docs.readthedocs.io/en/latest/first-steps/setup-3dcitydb.html
# at 1.3.3. Installation steps on PostgreSQL, step 3

# the postgres bin

# edit the connection details, considering that the importer/exporter are installed
gedit $HOME/3DCityDB-Importer-Exporter/3dcitydb/postgresql/ShellScripts/Unix/CONNECTION_DETAILS.sh

bash /home/kaue/3DCityDB-Importer-Exporter/3dcitydb/postgresql/ShellScripts/Unix/CONNECTION_DETAILS.sh

# RUNNING THE create_db
# will ask hor horizontal and height epsg codes, the same must be on "study case config" script at root folder
# begin session with the POSTGRES USER
bash  /home/kaue/3DCityDB-Importer-Exporter/3dcitydb/postgresql/ShellScripts/Unix/CREATE_DB.sh