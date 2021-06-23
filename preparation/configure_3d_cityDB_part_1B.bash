#!/bin/bash

# beginning at: https://www.vultr.com/docs/install-the-postgis-extension-for-postgresql-on-ubuntu-linux (look at part3)

# login to postgres superuser
sudo su - postgres



# crating another user
# createuser citydb_user

# altering password
# USER: citydb_user
# PASSWORD: citydb
# psql -c "alter user citydb_user with password 'citydb'"

# # create role
# ALTER ROLE citydb_user WITH SUPERUSER CREATEDB CREATEROLE LOGIN ENCRYPTED PASSWORD 'citydb';

# crating the database
createdb citydb_v4_3 -O postgres

# connecting to the database
psql -d citydb_v4_3

# postgres with a password
ALTER USER postgres PASSWORD 'postgres';

# https://3dcitydb-docs.readthedocs.io/en/latest/first-steps/setup-3dcitydb.html
# post gis extension (1.3.3. Installation steps on PostgreSQL, step 2)
CREATE EXTENSION postgis;

# optional that would need PostGIS SFCGAL extension.
# CREATE EXTENSION postgis_sfcgal;

# postgis raster extension
CREATE EXTENSION postgis_raster;


# list the users:
\du
# list databases:
\l+

# to made postgis avaliable on ohter schemas
# https://stackoverflow.com/a/63173336/4436950
ALTER DATABASE citydb_v4_3 SET search_path TO citydb, citydb_pkg, public;

# quit psql
exit

# RESTART POSTGRES
/etc/init.d/postgresql restart