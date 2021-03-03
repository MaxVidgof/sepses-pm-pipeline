#!/usr/bin/env python3.8
import sys

filename = sys.argv[1]

from pm4pymdl.objects.mdl.importer import importer as mdl_importer
from pm4pymdl.algo.mvp.gen_framework import algorithm as discovery
from pm4pymdl.visualization.mvp.gen_framework import visualizer as vis_factory

df = mdl_importer.apply(filename)

model = discovery.apply(df, model_type_variant="model1", node_freq_variant="type1", edge_freq_variant="type11")
gviz = vis_factory.apply(model, parameters={"format": "svg"})
vis_factory.view(gviz)

model = discovery.apply(df, model_type_variant="model2", node_freq_variant="type21", edge_freq_variant="type211")
gviz = vis_factory.apply(model, parameters={"format": "svg"})
vis_factory.view(gviz)

model = discovery.apply(df, model_type_variant="model3", node_freq_variant="type31", edge_freq_variant="type11")
gviz = vis_factory.apply(model, parameters={"format": "svg"})
vis_factory.view(gviz)
