import tudataset.tud_benchmark.auxiliarymethods.datasets as dp
from tudataset.tud_benchmark.auxiliarymethods.reader import tud_to_networkx
import networkx as nx
import walker as wk
import pickle
from random import choices



def generate_walk(dataset, walk_len):

    result = list()

    graph_list = read_graph_list(dataset)

    graph_list = choices(graph_list, k=5)

    for g in graph_list:
        temp = wk.random_walks(g, n_walks=5, walk_len=walk_len)

        temp_labels = dict()

        """
        g = nx.Graph()


        for i in range(walk_len -1):
            edge = (temp.item(i), temp.item(i+1))
            g.add_edge(*edge)

        """
        for k, v, attr in g.edges.data():
            temp_labels[(k, v)] = attr
            

        g = nx.Graph()        
        
        for i in range(walk_len -1):
            n1 = temp.item(i)
            n2 = temp.item(i+1)
            edge = (int(n1), int(n2))

            g.add_edge(*edge)

            try:
                nx.set_edge_attributes(g, {edge: temp_labels[(edge)]})
            except:
                nx.set_edge_attributes(g, {edge: temp_labels.get((n2, n1))})
        

        result.append(g)

    with open(f'input_size_{walk_len}.dat', "wb") as f:
        pickle.dump(result, f)


def read_input(size):
    with open(f'input_size_{size}.dat', "rb") as f:
        graph_list = pickle.load(f)

    return graph_list


def read_graph_list(dataset):
    try:
        G = tud_to_networkx(dataset)
    except:
        dp.get_dataset(dataset)
        G = tud_to_networkx(dataset)

    for g in G:
        for e in g.edges.data():
            e[2]["labels"] = e[2]["labels"][0]
    
    return G
    
