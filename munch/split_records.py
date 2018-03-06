import sys

data_dir = sys.argv[1]

train = open(data_dir + "/records-1-train.txt", "w")
valid = open(data_dir + "/records-2-valid.txt", "w")
test = open(data_dir + "/records-3-test.txt", "w")

with open(data_dir + "/records-clean.txt") as f:
    records = f.readlines()

    counter = 0
    for record in records:
        counter += 1
        fifth = counter % 5 + 1
        if fifth == 5:
            test.write(record)
        elif fifth == 4:
            valid.write(record)
        else:
            train.write(record)
