import networkx as nx
import tudataset.tud_benchmark.auxiliarymethods.datasets as dp
from tudataset.tud_benchmark.auxiliarymethods.reader import tud_to_networkx
import concurrent.futures
from in_out_data import generate_input, get_input
import itertools

BATCH = 5
NWKRS = 10

def generate_graphs():
    dataset = "MUTAG"
    dp.get_dataset(dataset)
    G = tud_to_networkx(dataset)

    generate_input(G, 3)

def read_graphs():
    G = get_input()

    return G

def compute_graph_batch(graph_list, input):
    graph_list = [{"graph": g, "line_graph":nx.line_graph(g)} for g in graph_list]
    input = {"graph":input, "line_graph": nx.line_graph(input)}

    return_list = list()

    for g in range(len(graph_list)):
        iso = nx.isomorphism.GraphMatcher(graph_list[g]["line_graph"], input["line_graph"])

        if iso.subgraph_is_isomorphic():
            return_list.append(graph_list[g]["graph"])


    return return_list
            

def compute_graph_list(input):

    graph_list = read_graphs()

    graph_list.append(1)
    it = iter(graph_list)
    G = list()
    
    g = ""

    while type(g) != int:
        
        batch_list = list()

        for _ in range(NWKRS):
            if(type(g) == int):
                break
            graph_batch = list()

            for _ in range(BATCH):
                g = next(it)

                if type(g) == int:
                    break
                graph_batch.append(next(it))

            batch_list.append(graph_batch)

            
        with concurrent.futures.ProcessPoolExecutor(NWKRS) as executor:
            futures = [
                executor.submit(compute_graph_batch, batch, input)
                for batch in batch_list
            ]

            for future in concurrent.futures.as_completed(futures):
                G.append(future.result())

    return G

def isomorfism_check() -> nx.Graph:



    return