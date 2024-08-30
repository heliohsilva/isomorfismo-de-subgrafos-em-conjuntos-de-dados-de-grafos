import csv
from scipy.stats import t,sem
import numpy as np

def media(numeros):

    temp = list(numeros.values())

    media = np.mean(temp)

    # confidence = nivel de confiança; df = graus de liberdade; loc = média; scale = erro padrão da média
    intervalo_de_confianca = t.interval(confidence=0.95, df=len(temp)-1,loc=media,scale=sem(temp))

    return [float(media), float(intervalo_de_confianca[0]), float(intervalo_de_confianca[1])]


def main():
    walk_size = []
    nworkers = []
    batch_size = []
    tempo = []
    size_e = []

    with open("result_bzr_sem_labels.csv", "r") as f:
        reader = csv.reader(f)
        next(reader) 

        for row in reader:
            walk_size.append(int(row[0]))
            nworkers.append(int(row[1]))
            batch_size.append(int(row[2]))
            size_e.append(int(row[4]))
            tempo.append(float(row[5]))
    

    it = iter(tempo)

    aux = []

    for i in range(0, len(size_e), 5):
        aux.append(size_e[i])
        
    matrix = dict()
    for i in [1, 2, 4, 8]:  #nworkers
        sub_matrix = dict()
        for j in [5, 15, 25]:  #batchsize
            arr = dict()
            for k in range(2, 19, 2):  #walk_size
                temp = dict()
                for l in range(5):
                    temp[l] = next(it)
                print(media(temp))
                arr[k] = media(temp)
            sub_matrix[j] = arr
        matrix[i] = sub_matrix

    nworkers_temp = nworkers
    batch_size_temp = batch_size
    walk_size_temp = walk_size

    nworkers = []
    batch_size = []
    walk_size = []

    for i in range(0, 540, 5):
        nworkers.append(nworkers_temp[i])
        batch_size.append(batch_size_temp[i])
        walk_size.append(walk_size_temp[i])

    it = iter(aux)

    with open("result_raw.csv", "a") as f:
                    f.write("nworkers, batch_size, walk_size, |E|, media de tempo, limite inferior, limete superior\n")
    for i in [1, 2, 4, 8]:  #nworkers
        for j in [5, 15, 25]:  #batchsize
            for k in range(2, 19, 2):  #walk_size
                aux = matrix[i][j][k]
                with open("result_raw.csv", "a") as f:
                    f.write(f'{i},{j},{k},{next(it)},{aux[0]},{aux[1]},{aux[2]}\n')



if __name__ == "__main__":
    main()  