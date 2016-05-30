#!/bin/bash
##########################
# 1. GAUL
# 2. Context
# 3. Cyclone
# 4. Drought
# 5. Flood
# 6. Landslide
##########################
DROP="/opt/drop/export/vagrant"
OP="replace"
##########################
# Exporting GAUL Data
echo
echo "Exporting GAUL Data"
LOCAL_PATH="data/gaul"
TABLES="gaul.admin0_polygons;gaul.admin1_polygons;gaul.admin2_polygons"
TABLES_SEP=";"
#fab dev \
#export_shapefiles:drop=$DROP,local_path=$LOCAL_PATH,tables=$TABLES,sep=$TABLES_SEP
##########################
# Exporting Context Data
echo
echo "Exporting Context Data"
LOCAL_PATH="data/context"
TABLES_SEP=";"
fab dev \
export_tables:drop=$DROP,local_path=$LOCAL_PATH,sep=$TABLES_SEP,op=$OP,tables="context.admin2_context" \
export_shapefiles:drop=$DROP,local_path=$LOCAL_PATH,sep=$TABLES_SEP,op=$OP,tables="context.admin2_polygons"
##########################
# Exporting Cyclone Data
echo
echo "Exporting Cyclone Data"
LOCAL_PATH="data/cyclone"
TABLES_SEP=";"
fab dev \
export_tables:drop=$DROP,local_path=$LOCAL_PATH,sep=$TABLES_SEP,op=$OP,tables="cyclone.admin2_popatrisk" \
export_shapefiles:drop=$DROP,local_path=$LOCAL_PATH,sep=$TABLES_SEP,op=$OP,tables="cyclone.events"
##########################
# Exporting Drought Data
echo
echo "Exporting Drought Data"
LOCAL_PATH="data/drought"
TABLES_SEP=";"
fab dev \
export_tables:drop=$DROP,local_path=$LOCAL_PATH,sep=$TABLES_SEP,op=$OP,tables="drought.admin2_popatrisk"
##########################
# Exporting Flood Data
echo
echo "Exporting Flood Data"
LOCAL_PATH="data/flood"
TABLES_SEP=";"
fab dev \
export_tables:drop=$DROP,local_path=$LOCAL_PATH,sep=$TABLES_SEP,op=$OP,tables="flood.admin2_popatrisk" \
export_shapefiles:drop=$DROP,local_path=$LOCAL_PATH,sep=$TABLES_SEP,op=$OP,tables="flood.events"
##########################
# Exporting Landslide Data
echo
echo "Exporting Landslide Data"
LOCAL_PATH="data/landslide"
TABLES_SEP=";"
fab dev \
export_shapefiles:drop=$DROP,local_path=$LOCAL_PATH,sep=$TABLES_SEP,op=$OP,tables="landslide.events"
