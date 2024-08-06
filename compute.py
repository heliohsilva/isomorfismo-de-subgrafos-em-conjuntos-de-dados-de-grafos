import networkx as nx
import concurrent.futures
from in_out_data import generate_walk, read_input, read_graph_list
import itertools

BATCH = 20
NWKRS = 5


def generate_input(dataset):
    for i in range(3, 10):
        generate_walk(dataset, i)



def compute_graph_list(dataset):

    graph_list = read_graph_list(dataset)

    #3, 8
    for i in range(3, 10):
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



def compute_graph_batch(graph_list, input):

    graph_list = [{"graph": g, "line_graph":nx.line_graph(g)} for g in graph_list]
    input = {"graph":input, "line_graph": nx.line_graph(input)}

    return_list = list()

    em = nx.isomorphism.numerical_node_match("labels", 456)

    for g in range(len(graph_list)):

        iso = nx.isomorphism.GraphMatcher(graph_list[g]["line_graph"], input["line_graph"], edge_match=em)

        if iso.subgraph_is_isomorphic():
            return_list.append(graph_list[g]["graph"])

    return return_list




def write_file(input_index, input_path_size, results):
    with open("iso_result.txt", "a") as f:
        f.write(f'o input número {input_index}, do tamanho {input_path_size} gerou {results} resultados\n')
