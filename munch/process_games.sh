#!/bin/bash

DATADIR="../data/"

# get game records
python get_records.py "$DATADIR"/bga-games-info.json > "$DATADIR"/records-all.txt

# remove rows that appear more than once
cat "$DATADIR"/records-all.txt | sort | uniq -u > "$DATADIR"/records-clean.txt

# create train/valid/test data sets
python split_records.py "$DATADIR"

python convert_records.py "$DATADIR"
