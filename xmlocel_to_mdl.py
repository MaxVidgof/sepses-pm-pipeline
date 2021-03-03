#!/usr/bin/env python3.8
import sys
print(sys.version)
from datetime import datetime
import ocel
import csv
import os

filename = sys.argv[1]

schema = os.path.join('..', 'ocel', 'ocel-support', 'schemas', 'schema.xml')
#construct ocel_log skeleton
#print("Validation successful: "+str(ocel.validate(filename, schema)))

ocel_log = ocel.import_log(filename)

#field names for (csv-like) mdl
field_names = ['event_id', 'event_activity', 'event_timestamp']
field_names.extend(['event_' + attr.split('#')[-1] for attr in ocel_log['ocel:global-log']['ocel:attribute-names']])
field_names.extend([type.split('#')[-1] for type in ocel_log['ocel:global-log']['ocel:object-types']])

with open(filename+'.mdl', 'w', newline='') as mdl:
	writer = csv.DictWriter(mdl, fieldnames=field_names)
	writer.writeheader()

	for event_id, event in ocel_log['ocel:events'].items():
		row = {'event_id':event_id, 'event_activity':event['ocel:activity'], 'event_timestamp':event['ocel:timestamp']}
		for attr, value in event['ocel:vmap'].items():
			row['event_'+attr.split('#')[-1]] = value
		for object in event['ocel:omap']:
			if ocel_log['ocel:objects'][object]['ocel:type'].split('#')[-1] not in row.keys():
				row[ocel_log['ocel:objects'][object]['ocel:type'].split('#')[-1]]=[]
			row[ocel_log['ocel:objects'][object]['ocel:type'].split('#')[-1]].append(object)
		print(row)
		writer.writerow(row)

