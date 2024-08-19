import compute as cp
import networkx as nx
import os
import sys

def main ():
    dataset = "MUTAG"

    #if os.path.exists("iso_result.txt"):
     #   os.remove("iso_result.txt")

    input_size = int(sys.argv[1])
    nworkers = int(sys.argv[2])
    batch_size = int(sys.argv[3])

    
    #cp.generate_input(dataset)
    cp.compute_graph_list(dataset=dataset, input_size=input_size, nworkers=nworkers, batch_size=batch_size)


if __name__ == "__main__":
    main()

