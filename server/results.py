hp = list("abcdefghi")
vp = list("987654321")

hw = list("abcdefghx")
vw = list("87654321x")


available_moves = []
for v in vw:
    for h in hw:
        available_moves.append(h + v + "h")

for v in vw:
    for h in hw:
        available_moves.append(h + v + "v")

for v in vp:
    for h in hp:
        available_moves.append(h + v)


p_rotations = {}
for i, val in enumerate(hp):
    p_rotations[val] = hp[8 - i]
for i, val in enumerate(vp):
    p_rotations[val] = vp[8 - i]

w_rotations = {}
for i, val in enumerate(hw[:8]):
    w_rotations[val] = hw[7 - i]
for i, val in enumerate(vw[:8]):
    w_rotations[val] = vw[7 - i]


def convert(pred):
    prob, move = pred
    return (move, int(prob * 1000))

def nonzero(pred):
    prob, move = pred
    return prob != 0

def order(predictions):
    preds = sorted(list(zip(predictions, available_moves)), reverse=True)
    filtered = filter(nonzero, map(convert, preds))

    return list(filtered)[:20]


def rotate(pred):
    move, prob = pred

    col = move[0]
    row = move[1]

    if len(move) == 3:
        newmove = w_rotations[col] + w_rotations[row] + move[2]
    elif len(move) == 2:
        newmove = p_rotations[col] + p_rotations[row]
    else:
        raise "oops"

    return (newmove, prob)
