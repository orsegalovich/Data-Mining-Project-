import itertools
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
from scipy.spatial import distance
import numpy


df = pd.read_csv('PairOfJudgesAndMutualCaseCount.csv', low_memory=False, na_filter=False)
G = nx.from_pandas_edgelist(df, source='judge_a', target='judge_b',
                            edge_attr='ratio')
edges = [(judge_a, judge_b) for (judge_a, judge_b, judges_dist) in G.edges(data=True) if judges_dist["ratio"] > 0.05]  # SET RATIO HERE
G.clear()
G.add_edges_from(edges)

path_length=dict(nx.all_pairs_shortest_path_length(G))

n = len(G.nodes())
distances=numpy.zeros((n,n))
labels_lst = list()
def calc_distances_of_graph():
    judge_a_counter = 0
    judge_b_counter = 0
    for judge_a, p in path_length.items():
        labels_lst.append(judge_a)
        judge_b_counter = judge_a_counter
        for judge_b, judges_dist in p.items():
            if judge_b_counter >= n:
                continue
            print(judge_a, judge_a_counter, judge_b, judge_b_counter, judges_dist)
            distances[judge_a_counter][judge_b_counter] = judges_dist
            distances[judge_b_counter][judge_a_counter] = judges_dist

            judge_b_counter +=1
        judge_a_counter+=1
calc_distances_of_graph()
sd = distance.squareform(distances)

hier = hierarchy.average(sd)

for  i, word in enumerate(labels_lst):
    f_let = word.split()[0][0]
    s_let = word.split()[1][0]
    labels_lst[i] = f_let+s_let


hierarchy.dendrogram(hier, labels=labels_lst, leaf_font_size=8)
plt.savefig(r'.\graph_pictures\hierarchy_by_paths_distance\hierarchy_by_paths_distance_005_threshold')
plt.show()