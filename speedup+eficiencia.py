import pandas as pd

def speedup(serial_time, parallel_time):
    return serial_time / parallel_time


def efficiency(speedup_value, nworkers):
    return speedup_value / nworkers


def parallel_fraction(speedup_value, nworkers):
    if nworkers == 1:
        return 0
    
    return (speedup_value - 1) / (nworkers - 1)


def karp_flatt_metric(speedup_value, nworkers):
    if speedup_value == nworkers:
        return 0
    
    return ((1/speedup_value)-(1/nworkers))/((1)-(1/nworkers))


def get_data():
    with open("result_raw.csv", "r") as f:
        data = f.read()


    lista = data.splitlines()
    lista.pop(0)
    
    pop_list = list()

    for index, line in enumerate(lista):
        if line == "":
            pop_list.append(index)

    i = 0
    
    for item in pop_list:
        lista.pop(int(item) - i)
        i +=1

    for i in range(len(lista)):
        lista[i] = lista[i].split(",")


    for item in lista:
        print(item[0])
        item[0] = int(item[0])
        item[1] = int(item[1])
        item[2] = int(item[2])
        item[4] = float(item[4])
        item.pop(5)
        item.pop(5)


    return lista


    
def main():

    lista = get_data()

    lista_1 = [item for item in lista if item[0] == 1] # sequencial
    lista_2 = [item for item in lista if item[0] == 2] # paralelo 
    lista_4 = [item for item in lista if item[0] == 4] # paralelo
    lista_8 = [item for item in lista if item[0] == 8] # paralelo

    print(lista_1)

    with open("speedup_eficiencia.csv", "a") as f:
        f.write("nworkers, batch_size, walk_size, speedup, eficiencia,fração, karp_flatt, |E|\n")


    for i in range(0, len(lista_1)):
        print(i)
        temp = dict()
        s = speedup(lista_1[i][4], lista_8[i][4])
        temp = {
            "s": s,
            "p" : parallel_fraction(s, 8),
            "k": karp_flatt_metric(s, 8),
            "e": efficiency(s, 8)
        }
        with open("speedup_eficiencia.csv", "a") as f:
            f.write(f'{8},{lista_1[i][1]},{lista_1[i][2]},{temp["s"]},{temp["e"]},{temp["p"]},{temp["k"]},{lista_1[i][3]}\n')

if __name__ == "__main__":
    main()