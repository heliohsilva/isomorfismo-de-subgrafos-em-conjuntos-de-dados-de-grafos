import compute as cp
import networkx as nx
import os

def main ():
    if os.path.exists("iso_result.txt"):
        os.remove("iso_result.txt")

    dataset = "MUTAG"
    #cp.generate_input(dataset)
    cp.compute_graph_list(dataset)


if __name__ == "__main__":
    main()

