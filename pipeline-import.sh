#!/bin/bash
##########################
# 0. Prepare Database
# 1. Admin District, Boundaries, etc.
# 2. Context
# 3. Cyclone
# 4. Drought
# 5. Flood
# 6. Landslide
# 7. Conflict (ACLED)
TARGET="dev"
DROP="/opt/drop"
OP="replace"
SRID="EPSG:4326"
#~/data/sparc/sparc2
#data
##########################
# Prepare Database
SCHEMAS="gaul;wfp;context;cyclone;flood;drought;landslide;conflict"
SCHEMAS_SEP=";"
fab $TARGET \
pipeline_sql_schemas:schemas=$SCHEMAS,sep=$SCHEMAS_SEP
##########################
# Reload Admin District, Boundaries, etc.
echo
echo "Reloading GAUL Data"
TYPE="MULTIPOLYGON"
# Import Admin 0
TABLE="gaul.admin0_polygons"
LOCAL_PATH="~/data/sparc/sparc2/gaul2015/wld_bnd_adm0_gaul_2015.*"
#fab $TARGET \
#shp:drop=$DROP,geometry_type=$TYPE,op=$OP,local_path=$LOCAL_PATH,table=$TABLE
# Import Admin 1
TABLE="gaul.admin1_polygons"
LOCAL_PATH="~/data/sparc/sparc2/gaul2015/wld_bnd_adm1_gaul_2015.*"
#fab $TARGET \
#shp:drop=$DROP,geometry_type=$TYPE,op=$OP,local_path=$LOCAL_PATH,table=$TABLE
## Import Admin 2
TABLE="gaul.admin2_polygons"
LOCAL_PATH="~/data/sparc/sparc2/gaul2015/wld_bnd_adm2_gaul_2015.*"
#fab $TARGET \
#shp:drop=$DROP,geometry_type=$TYPE,op=$OP,local_path=$LOCAL_PATH,table=$TABLE
# Rebuild Django Data
## Import WFP Presence Polygons
#fab $TARGET \
#shp:drop=$DROP,geometry_type=$TYPE,op=replace,local_path="data/wfp/wld_bnd_presence_wfp.*",table="wfp.presence_polygons"
# Rebuild Django Data
CHDIR="/home/sparc/sparc2.git"
TABLES="sparc2_sparccountry;wfppresencedjango_wfpcountry;lsibdjango_geographicthesaurusentry;gauldjango_gauladmin2;gauldjango_gauladmin1;gauldjango_gauladmin0"
#fab $TARGET \
#pipeline_sql_clear:tables=$TABLES,sep=";" \
#copy:src="data/lsib/lsib_thesaurus*",dest=$DROP \
#sql:drop=$DROP,local_path="code/countries_and_boundaries/gaul_raw2django.sql" \
#py:drop=$DROP,chdir=$CHDIR,local_path="code/countries_and_boundaries/reload_lsib.py" \
#sql:drop=$DROP,local_path="code/countries_and_boundaries/wfp_raw2django.sql" \
#py:drop=$DROP,chdir=$CHDIR,local_path="code/countries_and_boundaries/sparc_countries.py"
##########################
# Reload Context
echo
echo "Reloading Context Data"
SHP="data/context/25_05_2016_Context_layer.*"
TYPE="MULTIPOLYGON"
TABLE="context.admin2_polygons"
SQL="code/reload_context.sql"
fab $TARGET \
shp:drop=$DROP,geometry_type=$TYPE,op="replace",local_path=$SHP,table=$TABLE \
pipeline_sql_clear:tables="context.admin2_context",sep=";" \
sql:drop=$DROP,local_path=$SQL
##########################
# Reload Cyclone
echo
echo "Reloading Cyclone Data"
#SHP="~/data/sparc/sparc2/storms/*"
TYPE="POINT"
OP="append"
SRID="EPSG:4326"
#fab $TARGET \
#sql:cmd="DROP TABLE IF EXISTS cyclone.events;" \
#shp:drop=$DROP,geometry_type=$TYPE,op=$OP,srid=$SRID,local_path="data/cyclone/cyclone_events.*",table="cyclone.events" \
#sql:drop=$DROP,local_path="code/disasters/reload_cyclones.sql" \
#import_tables:drop=$DROP,op="replace",local_path="data/cyclone/cyclone_admin2_popatrisk.csv",table="cyclone.admin2_popatrisk"
##########################
# Reload Drought
echo
echo "Reloading Drought Data"
TYPE="POINT"
OP="append"
SRID="EPSG:4326"
#fab $TARGET \
#sql:drop=$DROP,local_path="code/disasters/reload_drought.sql" \
#import_tables:drop=$DROP,op="replace",local_path="data/drought/drought_admin2_popatrisk.csv",table="drought.admin2_popatrisk"
##########################
# Reload Flood
echo
echo "Reloading Flood Data"
#SHP="~/data/sparc/sparc2/storms/*"
TYPE="POINT"
OP="append"
#fab $TARGET \
#sql:cmd="DROP TABLE IF EXISTS flood.events;" \
#shp:drop=$DROP,geometry_type=$TYPE,op=$OP,srid=$SRID,local_path="data/flood/flood_events.*",table="flood.events" \
#sql:drop=$DROP,local_path="code/disasters/reload_flood.sql" \
#import_tables:drop=$DROP,op="replace",local_path="data/flood/flood_admin2_popatrisk.csv",table="flood.admin2_popatrisk"
##########################
# Reload Landslide
echo
echo "Reloading Landslide Data"
#fab $TARGET \
#sql:cmd="DROP TABLE IF EXISTS landslide.events;" \
#shp:drop=$DROP,geometry_type="POINT",op="replace",local_path="data/landslide/landslide_events.*",table="landslide.events" \
#sql:cmd="DROP TABLE IF EXISTS landslide.admin2_popatrisk;" \
#shp:drop=$DROP,geometry_type="MULTIPOLYGON",op="replace",local_path="data/landslide/26_05_2016_Landslide_Workshop.*",table="landslide.admin2_polygons" \
#sql:drop=$DROP,local_path="code/disasters/reload_landslide_schema.sql" \
#sql:drop=$DROP,local_path="code/disasters/reload_landslide_data.sql"
##########################
# Reload Landslide
echo
echo "Clearing In-Memory Cache"
CACHES="11212"
#fab $TARGET memcached_clear:caches=$CACHES,sep=";"
