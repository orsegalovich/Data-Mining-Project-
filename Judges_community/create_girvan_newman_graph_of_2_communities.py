import itertools

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms.community.centrality import girvan_newman
from random import random


df = pd.read_csv('..\PairOfJudgesAndMutualCaseCount.csv', low_memory=False, na_filter=False)
G = nx.from_pandas_edgelist(df, source='judge_a', target='judge_b',
                            edge_attr='ratio')


edges = [(u, v) for (u, v, d) in G.edges(data=True) if d["ratio"] > 0.05]  # SET RATIO HERE
G.clear()
G.add_edges_from(edges)


comp = nx.algorithms.community.girvan_newman(G)
k = 4
# limited = itertools.takewhile(lambda c: len(c) <= k, comp)
# communities = list(limited)[-1]
#
# community_dict = {}
# community_num = 0
# for community in communities:
#     for character in community:
#         community_dict[character] = community_num
#         community_num += 1
#         nx.set_node_attributes(G, community_dict, 'community')
#
# betweenness_dict = nx.betweenness_centrality(G) # Run betweenness centrality
#
# nx.set_node_attributes(G, betweenness_dict, 'betweenness')
#
# color = 0
# color_map = ['red', 'blue', 'yellow', 'purple', 'black', 'green', 'pink']
# for community in communities:
#     nx.draw(G, pos = nx.spring_layout(G, iterations=200), nodelist = community, node_size = 100, node_color = color_map[color])
#     color += 1
#
# plt.show()


#
# posi_gn = nx.spring_layout(G)
#
# comp = girvan_newman(G)
#
#
# k = 3   # number of communities
# for _ in range(k-1):
#     comms = next(comp)
#
#
#
# colors = 'rgb'
# for nodes, c in zip(comms, colors):
#     nx.draw_networkx_nodes(G, posi_gn, nodelist=nodes, node_color=[c], with_labels=True, arrows=True, font_color='gray')
# nx.draw_networkx_edges(G, posi_gn, with_labels=True)

# plt.show()













node_groups = []
for com in next(comp):
  node_groups.append(list(com))

print(node_groups)

color_map = []
for node in G:
    if node in node_groups[0]:
        color_map.append('blue')
    else:
        color_map.append('green')


pos = nx.spring_layout(G, seed=7, k=0.3, iterations=20)  # positions for all nodes - seed for reproducibi


nx.draw(G, pos, font_size=8, font_family="sans-serif", node_color=color_map, with_labels=True)

plt.savefig(r'.\graph_pictures\grivan_newman\2_groups_005_threshold')
plt.show()