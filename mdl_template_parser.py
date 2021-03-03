#!/usr/bin/env python3.8
import sys
import csv
import json

filename = sys.argv[1]
template_f = sys.argv[2]

with open(template_f, 'r') as r:
	templates = json.load(r)


with open(filename) as f:
	r = csv.reader(f, delimiter=',')
	#h = next(r, None)
	lines = list(r)

for i in range(1,len(lines)):
	lines[i][1] = templates['templates'][lines[i][1]]

with open(filename.replace('.mdl', '_templated.mdl'), 'w') as w:
	writer = csv.writer(w, delimiter=',')
	writer.writerows(lines)
