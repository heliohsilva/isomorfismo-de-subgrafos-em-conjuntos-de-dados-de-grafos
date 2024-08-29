if [ -e "result.csv" ]
then
    rm result.csv
fi

if [ -e "iso_result.txt" ]
then
    rm iso_result.txt
fi

echo "walk_size, nworkers, batch_size, |V|, |E|, tempo, memoria" >> result.csv


for nworkers in 1 2 4 8
do
    for batch_size in 5 15 25
    do
        for walk_size in 2 4 6 8 10 12 14 16 18
        do
            for i in $(seq 1 5)
            do
                echo -n "$walk_size,$nworkers,$batch_size," >> result.csv
                memory=$( /usr/bin/time -f"%M" python main.py $walk_size $nworkers $batch_size 2>&1 /dev/null )
                echo "$memory" >> result.csv
            done
        done
    done
done
