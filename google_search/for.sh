#!/bin/bash
for i in `seq 1 500`
do
    python extract_meta_texts.py $i
done
