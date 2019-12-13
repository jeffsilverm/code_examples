#! /bin/bash
#
# A program to exercise the CommTech demo
#
OUTPUT_FILE="CommTech_demo.dat"
for recs in 5 50 500 5000 50000; do
  # Empirically, the number of fields cannot get much larger than 250.  300 is
  # too large
  for fields in 4 40 200 250; do
    echo -n "$recs $fields  |">> $OUTPUT_FILE
    /usr/bin/time -f " %U secs" --append --output=$OUTPUT_FILE \
        python3 CommTech_demo.py $recs $fields
  done
done
