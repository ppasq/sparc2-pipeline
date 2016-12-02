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
TARGET="prod"
DROP="/opt/drop"
OP="replace"
SRID="EPSG:4326"
##########################
# Reload Drought
#import_tables:drop=$DROP,op="replace",local_path="data/drought/new_drought_march_amended.csv",table="drought.admin2_raw" \
echo
echo "Reloading Drought Data"
TYPE="POINT"
OP="append"
SRID="EPSG:4326"
#fab $TARGET \
#sql:cmd="DROP TABLE IF EXISTS drought.raw;" \
#sql:drop=$DROP,local_path="code/disasters/reload_drought_schema.sql" \
#import_tables:drop=$DROP,op="replace",local_path="data/drought/drought_all.csv",table="drought.admin2_raw" \
#pipeline_sql_clear:tables="drought.admin2_popatrisk",sep=";" \
#sql:drop=$DROP,local_path="code/disasters/reload_drought_data.sql"

#drought_all.csv

fab $TARGET \
sql:cmd="DROP TABLE IF EXISTS drought.raw;" \
sql:drop=$DROP,local_path="code/disasters/reload_drought_schema.sql" \
import_tables:drop=$DROP,op="replace",local_path="data/drought/new_drought_march_amended.csv",table="drought.admin2_raw" \
pipeline_sql_clear:tables="drought.admin2_popatrisk",sep=";" \
sql:drop=$DROP,local_path="code/disasters/reload_drought_data.sql"
