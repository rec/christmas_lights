while true
do
    bp run --verbose base.yml + bpx-600.yml + projects/random-walk.yml &
    sleep 1200
    bp-kill
    sleep 2
done
