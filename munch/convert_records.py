from mutable import Converter

import numpy as np
import h5py
import sys

data_dir = sys.argv[1]

c = Converter()

def add_to_set(dset, data, inx_prev):
    inx_cur = inx_prev + len(data)
    print(inx_prev, inx_cur)
    dset[inx_prev:inx_cur] = data

    return inx_cur

def convert_set(path, hf):
    print()
    print(path)
    records = open(path)

    games = records.readlines()
    moves = sum([(record.count(";") + 1) for record in games])
    print(len(games))
    print(moves)

    dset = hf.create_dataset("samples", shape=(moves, 9, 9, 9), dtype=np.uint8)

    cur = 0
    inx_prev = 0
    data = []
    for record in games:
        cur += 1
        data.extend(c.convert(record.strip()))
        if cur % 1000 == 0:
            inx_prev = add_to_set(dset, data, inx_prev)
            data = []

    add_to_set(dset, data, inx_prev)

def convert_all():
    data_sets = [
        "records-1-train",
        "records-2-valid",
        "records-3-test",
    ]

    for ds in data_sets:
        with h5py.File("%s%s.h5" % (data_dir, ds), "w") as hf:
            convert_set("%s%s.txt" % (data_dir, ds), hf)

convert_all()
