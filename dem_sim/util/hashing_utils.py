def commutative_cantor(i, j):
    i = int(i)
    j = int(j)
    i, j = sorted([i, j])
    return (i + j) * (i + j + 1) / 2 + j

    # TODO: Test other hashing functions.
