from polka.tools import calculate_routeid, print_poly


def _main():
    print("Insering irred poly (nodeID)")
    s = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    ]
    o = [
        [1, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
    ]

    for i in range(2, 11):
        print("####### H1 -> H{}".format(i))
        o_idx = i - 1
        o_aux = o[0:o_idx]
        o_aux.append([1])
        print(o_aux)
        print_poly(calculate_routeid(s[0:i], o_aux, debug=False))

    o = [
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 0],
    ]

    for i in range(2, 11):
        print("####### H{} -> H1".format(12 - i))
        o_idx = i - 1
        rev_s = list(reversed(s))
        o_aux = o[0:o_idx]
        o_aux.append([1])
        print(o_aux)
        print_poly(calculate_routeid(rev_s[0:i], o_aux, debug=False))


if __name__ == "__main__":
    _main()
