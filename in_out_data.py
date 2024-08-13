import tudataset.tud_benchmark.auxiliarymethods.datasets as dp
from tudataset.tud_benchmark.auxiliarymethods.reader import tud_to_networkx
import networkx as nx
import walker as wk
import pickle
from random import choices

#walk_len refere-se ao numero de nodes


def start_node_choice(g):
    return choices(g, k=1)


def generate_walk(dataset, walk_len):

    result = list()

    graph_list = choices(read_graph_list(dataset), k=5)

    for g in graph_list:
        start_node = start_node_choice(list(g.nodes))

        #n_walks: quantidade de caminhos gerados
        #walk_len: quantidade de nodes contidos no caminho
        #start_nodes: lista com os nodes de inicio de cada caminho
        temp = wk.random_walks(g, n_walks=1, walk_len=walk_len, start_nodes=[start_node[0]]) 

        temp_g = nx.Graph()        
        
        for i in range(walk_len -1):
            n1 = temp.item(i)
            n2 = temp.item(i+1)
            
            for e in g.edges([n1, n2], data=True):
                temp_g.add_edge(*e[:2], **e[2])


        for n in g.nodes.data():
            if n[0] == n1 or n[0] == n2:
                temp_g.add_node(*n[:1], **n[1])
        
        result.append(temp_g)


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

    #as labels sao dadas em listas. eo codigo abaixo transforma estas listas em int
    for g in G:
        for e in g.edges.data():
            e[2]["labels"] = e[2]["labels"][0]
        
        for n in g.nodes.data():
            n[1]["labels"] = n[1]["labels"][0]
    
    return G
    
