#!/bin/bash

# beginning at: https://www.vultr.com/docs/install-the-postgis-extension-for-postgresql-on-ubuntu-linux (look at part3)

# login to postgres superuser
sudo su - postgres

# crating another user
createuser citydb_user

# altering password
# USER: citydb_user
# PASSWORD: citydb
psql -c "alter user citydb_user with password 'citydb'"

# crating the database
createdb citydb_v4 -O citydb_user

# connecting to the database
psql -d citydb_v4

# https://3dcitydb-docs.readthedocs.io/en/latest/first-steps/setup-3dcitydb.html
# post gis extension (1.3.3. Installation steps on PostgreSQL, step 2)
CREATE EXTENSION postgis;

# optional that would need PostGIS SFCGAL extension.
# CREATE EXTENSION postgis_sfcgal;

# postgis raster extension
CREATE EXTENSION postgis_raster;