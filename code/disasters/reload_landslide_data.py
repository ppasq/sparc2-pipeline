from geodash.enumerations import MONTHS_SHORT3

from geodash.data import GeoDashDatabaseConnection

print "Inserting Landslide Data..."
print "..."
print ""

prob_classes = [
  {'input': 'low', 'output_text': 'low', "output_int": 1},
  {'input': 'medium', 'output_text': 'medium', "output_int": 2},
  {'input': 'high', 'output_text': 'high', "output_int": 3},
  {'input': 'very_h', 'output_text': 'very_high', "output_int": 4}
]

tpl = None
with open('insert_landslide_data.tpl.sql', 'r') as f:
    tpl = f.read()

with GeoDashDatabaseConnection() as geodash_conn:
    try:
        geodash_conn.exec_update("DELETE FROM landslide.admin2_popatrisk;")
    except:
        pass
    for month in MONTHS_SHORT3:
        for prob_class in prob_classes:
            # Population at Risk Data
            sql = tpl.format(** {
                'month': month,
                'prob_class_input': prob_class['input'],
                'prob_class_output_text': prob_class['output_text'],
                'prob_class_output_int': str(prob_class['output_int'])
            })
            geodash_conn.exec_update(sql)

print "Done Inserting Landslide Data"
