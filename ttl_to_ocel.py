#!/usr/bin/env python3.8
import sys
print(sys.version)
#import pm4py
#from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from datetime import datetime
from pprint import pprint
from rdflib import Graph
import rdflib
#import xes
import ocel
import os

schema = os.path.join('..', 'ocel', 'ocel-support', 'schemas', 'schema.xml')
#construct ocel_log skeleton

ocel_log = {}
ocel_log['ocel:global-log']={
	'ocel:attribute-names': [],
	'ocel:object-types': [],
	'ocel:version': '0.1',
	'ocel:ordering': 'timestamp'
}
ocel_log['ocel:global-event']={'id': '__INVALID__', 'activity': '__INVALID__', 'timestamp':'__INVALID__', 'omap':'__INVALID__'}
ocel_log['ocel:global-object']={'id': '__INVALID__', 'type': '__INVALID__'}
ocel_log['ocel:events']={}
ocel_log['ocel:objects']={}

structure = []

filename = "small/access.log.0.ttl" #access.log.0.ttl  #"logs_20200425/apache-access.log_structured.ttl"
classname = "log:Event"  #"core:Log"
ts_predicate = "log:time" #"core:timestamp"
act_predicate = "logex:template" #"slog:templateId"

g = Graph()

g.parse(filename, format="turtle")
#print(filename)
print(str(len(g)))

i = 0
for stmt in g:
	if i < 2:
		pprint(stmt)
		i += 1
	else:
		break


rdf_events = g.query(
	f"""SELECT ?evt ?ts ?act ?y ?z
	WHERE {{
		?evt a {classname} .
		?evt {ts_predicate} ?ts.
		?evt {act_predicate} ?act .
		?evt ?y ?z .
	}}""")

#		FILTER ( !sameTerm(?y, {ts_predicate}) && !sameTerm(?y, a) && !sameTerm(?y, {act_predicate}) )


print(str(len(rdf_events)))
i = 0
for evt, ts, act, y, z in rdf_events:
	print("Event: " + str(act)+" at "+str(ts))
	print(str(i)+"/"+str(len(rdf_events)))
	i += 1
	if(str(evt) not in ocel_log['ocel:events'].keys()):
		ocel_log['ocel:events'][str(evt)] = {
			'ocel:timestamp': datetime.fromisoformat(str(ts)),
			'ocel:activity': str(act),
			'ocel:omap':[],
			'ocel:vmap':{}}
	if(type(z)==rdflib.URIRef):
		#object
		ocel_log['ocel:events'][str(evt)]['ocel:omap'].append(z)
		if (str(y) not in ocel_log['ocel:global-log']['ocel:object-types']):
			ocel_log['ocel:global-log']['ocel:object-types'].append(str(y))
		if (str(z) not in ocel_log['ocel:objects'].keys()):
			ocel_log['ocel:objects'][str(z)]= {'ocel:type': str(y), 'ocel:ovmap':{}}
	elif(type(z)==rdflib.Literal):
		#attribute
		ocel_log['ocel:events'][str(evt)]['ocel:vmap'][str(y)]=str(z)
		if (str(y) not in ocel_log['ocel:global-log']['ocel:attribute-names']):
			ocel_log['ocel:global-log']['ocel:attribute-names'].append(str(y))
	else:
		#???
		pass

query = """SELECT ?obj ?y ?z
	WHERE {
		?obj ?y ?z
		FILTER (
			!EXISTS {
				?obj a """ + classname + """ .
			}
		)
	}"""
print(query)
rdf_objects = g.query(query)


print(str(len(rdf_objects)))
i = 0
for obj, y, z in rdf_objects:
	print("Object: "+str(obj))
	print(str(i)+"/"+str(len(rdf_objects)))
	i += 1
	if(str(obj) not in ocel_log['ocel:objects'].keys()):
		ocel_log['ocel:objects'][str(obj)] = {
			'ocel:type': ocel_log['ocel:global-object']['type'],
			'ocel:ovmap':{}}
	if(type(z)==rdflib.Literal):
		#attribute
		ocel_log['ocel:objects'][str(obj)]['ocel:ovmap'][str(y)]=str(z)
		if (str(y) not in ocel_log['ocel:global-log']['ocel:attribute-names']):
			ocel_log['ocel:global-log']['ocel:attribute-names'].append(str(y))
	elif(type(z)==rdflib.URIRef):
		#relation to other object
		#keep as attribute just in case
		#TODO: rework
		ocel_log['ocel:objects'][str(obj)]['ocel:ovmap'][str(y)]=str(z)
		if (str(y) not in ocel_log['ocel:global-log']['ocel:attribute-names']):
			ocel_log['ocel:global-log']['ocel:attribute-names'].append(str(y))
	else:
		#???
		pass

ocel.export_log(ocel_log, filename+".xmlocel")
print("Validation successful: "+str(ocel.validate(filename+".xmlocel", schema)))

