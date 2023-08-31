for d in 5 50 100;
do
    for n in 1 2 3;
    do
        echo "./main 50 $d $n > out.ppm"
        command time ./main 50 $d $n > out.ppm
    done
done