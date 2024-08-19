for walk_size in {3..7}
do
    for batch_size in 5 10 15 20
    do
        for nworkers in 1 2 4 6 8
        do
            echo "walk_size: $walk_size, nworkers: $nworkers, batch_size: $batch_size" >> result.txt
            #/usr/bin/time -v python main.py $walk_size $nworkers $batch_size 2>&1 | tee  -a result.txt
            python main.py $walk_size $nworkers $batch_size
        done
    done
done