import compute as cp
import networkx as nx

def main ():
    g = nx.Graph()

    g.add_edge(0, 1)
    #g.add_edge(1, 2)
    
    G = cp.compute_graph_list(g)

    for graph in G:
        for gr in graph:
            print(gr)

if __name__ == "__main__":
    main()