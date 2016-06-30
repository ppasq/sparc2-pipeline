# Run this inside your sparc virutal enviornment on the actual server
#
import requests
import sys
import time

from geosite.data import GeositeDatabaseConnection

from sparc2.data import data_local_country_admin
from sparc2.enumerations import URL_VAM

import django
django.setup()

SLEEP_PERIOD = 0.5

results = {}
with GeositeDatabaseConnection() as geosite_conn:

    q = "SELECT LSIB.iso_alpha3 as iso_alpha3 FROM lsibdjango_geographicthesaurusentry as LSIB LEFT JOIN gauldjango_gauladmin0 as G ON LSIB.gaul = G.admin0_code LEFT JOIN wfppresencedjango_wfpcountry as W ON LSIB.id = W.thesaurus_id WHERE LSIB.iso_alpha3 IS NOT NULL and W.id IS NOT NULL GROUP BY LSIB.iso_alpha3, G.admin0_code, G.admin0_name ORDER BY LSIB.iso_alpha3;"
    geosite_conn.cursor.execute(q)
    countries = geosite_conn.cursor.fetchall()

    for r in countries:
        iso_alpha3 = r[0]
        collection = data_local_country_admin().get(cursor=geosite_conn.cursor, iso_alpha3=iso_alpha3, level=1)
        if collection.get("features", None):
            for feature in collection.get("features", None):
                admin0_code = feature["properties"]["admin0_code"]
                admin0_name = feature["properties"]["admin0_name"]
                admin1 = feature["properties"]["admin1_code"]

                hasFCS = False
                try:
                    response = requests.get(url=URL_VAM["FCS"].format(admin0=admin0_code, admin1=admin1))
                    vam_data_fcs = response.json()
                    hasFCS = vam_data_fcs and len(vam_data_fcs) > 0
                except:
                    hasFCS = False

                hasCSI = False
                try:
                    response = requests.get(url=URL_VAM["CSI"].format(admin0=admin0_code, admin1=admin1))
                    vam_data_csi = response.json()
                    hasCSI = vam_data_csi and len(vam_data_csi) > 0
                except:
                    hasCSI = False

                if iso_alpha3 not in results:
                    results[iso_alpha3] = {
                        "iso_alpha3": iso_alpha3,
                        "admin0_code": admin0_code,
                        "admin0_name": admin0_name,
                        "fcsCount": 0,
                        "csiCount": 0,
                        "admin1": []
                    }

                results[iso_alpha3]["admin1"].append({
                    "admin1": admin1,
                    "hasFCS": hasFCS,
                    "hasCSI": hasCSI
                })

        time.sleep(SLEEP_PERIOD)

for iso_alpha3 in results:
    results[iso_alpha3]["fcsCount"] = len([x for x in results[iso_alpha3]["admin1"] if x['hasFCS']])
    results[iso_alpha3]["csiCount"] = len([x for x in results[iso_alpha3]["admin1"] if x['hasCSI']])

results_ordered = sorted([value for key, value in results.iteritems()], key=lambda x: x.get('iso_alpha3', None))
print "\t".join(["iso_alpha3", "admin0_code", "admin0_name", "FCS", "CSI"])
for r in results_ordered:
    print "\t".join([
        r["iso_alpha3"],
        str(r["admin0_code"]),
        r["admin0_name"],
        str(r["fcsCount"]),
        str(r["csiCount"])
    ])
