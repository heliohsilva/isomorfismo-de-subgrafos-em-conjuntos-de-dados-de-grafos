import networkx as nx
import concurrent.futures
from in_out_data import generate_walk, read_input, read_graph_list
import itertools
from random import choices
import matplotlib.pyplot as plt
import time

BATCH = 20
NWKRS = 5

def generate_input(dataset):
    for i in range(3, 8):
        generate_walk(dataset, i)


def compute_graph_list(dataset, input_size, nworkers, batch_size):
    input_list = read_input(input_size)

    #cada input_file tem 5 input graphs.
    for j in range(5):
        input = input_list[j]
        it, graph_list_size = read_graph_list(dataset)
        begin = time.time()
        
        batch_size = int(graph_list_size * (batch_size/100))
        iso_G = list()
        verifica = 0
        
        g = ""

        while type(g) != int:
            batch_list = list()
            temporary_result = list()
            for _ in range(nworkers):
                if type(g) == int:
                    break
                graph_batch = list()
                for _ in range(batch_size):
                    g = next(it, 1)
                    if type(g) == int:
                        break
                    graph_batch.append(g)
            
                batch_list.append(graph_batch)
                verifica += len(graph_batch)
                
            with concurrent.futures.ProcessPoolExecutor(nworkers) as executor:
                futures = [
                    executor.submit(compute_graph_batch, batch, input)
                    for batch in batch_list
                ]
                for future in concurrent.futures.as_completed(futures):
                    temporary_result.append(future.result())
            result_iter = itertools.chain(*temporary_result)
            if result_iter:
                for graph in result_iter:
                    iso_G.append(graph)

        print(verifica)

        write_file(j, input_size, len(iso_G), time.time() - begin, nworkers, batch_size)


def parse_line_graph(g):

    G = nx.Graph(nx.line_graph(g))

    for n in G.nodes():
        G.nodes[n]["labels"] = g[n[0]][n[1]]["labels"]

    return G

def compute_graph_batch(graph_list, input):

    graph_list = [{"graph": g, "line_graph": parse_line_graph(g)} for g in graph_list]
    input = {"graph":input, "line_graph": parse_line_graph(input)}

    return_list = list()

    nm = nx.isomorphism.numerical_node_match('labels', -1)

    for g in range(len(graph_list)):
        iso = nx.isomorphism.GraphMatcher(graph_list[g]["line_graph"], input["line_graph"], node_match=nm)
        if iso.subgraph_is_isomorphic():
            return_list.append(graph_list[g]["graph"])

    if return_list:
        teste = choices(return_list, k=1)[0]
        """
        input = input["graph"]
        pos = nx.spring_layout(input)  
        nx.draw(input, pos, with_labels=True)
        edge_labels = nx.get_edge_attributes(input, 'labels')

        nx.draw_networkx_edge_labels(input, pos, edge_labels=edge_labels, label_pos=0.5)

        plt.show()

        pos = nx.spring_layout(teste)  

        nx.draw(teste, pos, with_labels=True)

        edge_labels = nx.get_edge_attributes(teste, 'labels')
        nx.draw_networkx_edge_labels(teste, pos, edge_labels=edge_labels, label_pos=0.5)

        plt.show()
        """
        
    else:
        print("sem resultado\n")

    return return_list



def write_file(input_index, input_path_size, results, time, nworkers, batch_size):
    with open("iso_result.txt", "a") as f:
        f.write(f'o input número {input_index}, do tamanho {input_path_size} gerou {results} resultados e demorou {time} segundos para processar\n')
        f.write(f'trabalharam neste processo {nworkers} cpus e o batch tinha tamanho {batch_size}\n\n')

