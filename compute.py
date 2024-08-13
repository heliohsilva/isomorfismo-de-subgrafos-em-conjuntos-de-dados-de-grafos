import networkx as nx
import concurrent.futures
from in_out_data import generate_walk, read_input, read_graph_list
import itertools
from random import choices
import matplotlib.pyplot as plt
from memory_profiler import profile

BATCH = 20
NWKRS = 5

def generate_input(dataset):
    for i in range(3, 8):
        generate_walk(dataset, i)


def compute_graph_list(dataset):
    
    graph_list = read_graph_list(dataset)

    #3, 8
    for i in range(3, 8):
        input_list = read_input(i)

        #5
        for j in range(5):

            input = input_list[j]

            graph_list.append(1)
            it = iter(graph_list)
            G = list()
            
            g = ""

            while type(g) != int:
                
                batch_list = list()
                temporary_result = list()

                for _ in range(NWKRS):
                    if type(g) == int:
                        break
                    graph_batch = list()

                    for _ in range(BATCH):
                        g = next(it)

                        if type(g) == int:
                            break
                        graph_batch.append(g)
                
                

                    batch_list.append(graph_batch)
                    
                with concurrent.futures.ProcessPoolExecutor(NWKRS) as executor:
                    futures = [
                        executor.submit(compute_graph_batch, batch, input)
                        for batch in batch_list
                    ]

                    for future in concurrent.futures.as_completed(futures):
                        temporary_result.append(future.result())

                result_iter = itertools.chain(*temporary_result)

                if result_iter:
                    for graph in result_iter:
                        G.append(graph)

            write_file(j, i, len(G))


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



def write_file(input_index, input_path_size, results):
    with open("iso_result.txt", "a") as f:
        f.write(f'o input número {input_index}, do tamanho {input_path_size} gerou {results} resultados\n')
