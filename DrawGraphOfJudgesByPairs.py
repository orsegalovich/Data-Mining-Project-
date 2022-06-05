import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('PairOfJudgesAndMutualCaseCount.csv', low_memory=False, na_filter=False)
G = nx.from_pandas_edgelist(df, source='judge_a', target='judge_b',
                            edge_attr='appearances')

widths = np.array([w for *_, w in G.edges.data('appearances')])

pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibi

# nodes
nx.draw_networkx_nodes(G, pos, node_size=600)

# edges
nx.draw_networkx_edges(G, pos, width=widths/1000)  # using a 10x scale factor here

# labels
nx.draw_networkx_labels(G, pos, font_size=7, font_family="sans-serif")

ax = plt.gca()
ax.margins(0.03)
plt.axis("off")
plt.tight_layout()
plt.savefig('.\Judges_connection_by_cases_calculated_by_pairs')
