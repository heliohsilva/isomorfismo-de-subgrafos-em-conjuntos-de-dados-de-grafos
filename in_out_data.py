import networkx as nx
import walker as wk
import pickle

def generate_input(graph_list, walk_len):

    result = list()
    i = -1

    for g in graph_list:
        i += 1
        temp = wk.random_walks(g, n_walks=1, walk_len=walk_len)
        temp_labels = dict()

        for k, v, attr in g.edges.data():
            temp_labels[(k, v)] = attr

        g = nx.Graph()        
        
        for i in range(walk_len -1):
            n1 = temp.item(i)
            n2 = temp.item(i+1)
            edge = (n1, n2)

            g.add_edge(*edge)

            try:
                nx.set_edge_attributes(g, {edge: temp_labels[(edge)]})
            except:
                nx.set_edge_attributes(g, {edge: temp_labels.get((n2, n1))})

        result.append(g)

    with open("input.dat", "wb") as f:
        pickle.dump(result, f)


def get_input():
    with open("input.dat", "rb") as f:
        graph_list = pickle.load(f)

    return graph_list