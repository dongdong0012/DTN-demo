import os
import json
"""
pheme
{
    "n": 5802,
    "p": 97410,
    "u": 49778
}

"""

def stats(in_dir, node_types, edge_files):
    nodes = {t : [] for t in node_types}
    for (t0, t1), fname in edge_files.items():
        with open(os.path.join(in_dir, fname), 'r') as f:
            for line in f.readlines():
                info = line.strip().split()
                nodes[t0].append(info[0])
                nodes[t1].append(info[1])
    counts = {k : len(set(v)) for k, v in nodes.items()}
    return counts
dataset = 'pheme'
prefix = 'pheme_'
in_dir = 'PHEME/graph_def'
edge_dir = in_dir
node_types = ['n', 'p', 'u']
edge_files = {
    ('n', 'p'): 'PhemeNewsPost.txt',
    ('n', 'u'): 'PhemeNewsUser.txt',
    ('p', 'p'): 'PhemePostPost.txt',
    ('p', 'u'): 'PhemePostUser.txt',
    ('u', 'u'): 'PhemeUserUser.txt',
}
edges_to_enforce = {('n', 'u'), ('p', 'u'),}

counts = stats(in_dir, node_types, edge_files)
print(dataset)
print(json.dumps(counts, indent=4))