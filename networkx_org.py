import pandas as pd
import networkx as nx

df = pd.read_csv("edges.csv")
#print(df)
orgchart=nx.from_pandas_edgelist(df,source='from',target='to')
p=nx.drawing.nx_pydot.to_pydot(orgchart)
p.write_png('orgchart.png')



