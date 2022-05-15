#!/usr/bin/env python3
from polka.tools import calculate_routeid, print_poly
DEBUG = False


def _main():
    print("Insering irred poly (node-ID)")
    s = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1],  # s1
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],  # s2
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],  # s3
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],  # s4
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],  # s5
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],  # s6
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],  # s7
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1],  # s8
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1],  # s9
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1],  # s10
    ]
    print("From h1 to h3 ====")
    # defining the nodes from h1 to h3
    nodes = [
        s[0],
        s[1],
        s[2]
    ]
    # defining the transmission state for each node from h1 to h3
    o = [
        [1, 0],     # s1
        [1, 0, 0],  # s2
        [1],        # s3
    ]
    print_poly(calculate_routeid(nodes, o, debug=DEBUG))

    print("From h3 to h1 ====")
    # defining the nodes from h1 to h3
    nodes = [
        s[2],
        s[1],
        s[0]
    ]
    # defining the transmission state for each node from h1 to h3
    o = [
        [1, 0],     # s3
        [1, 0],     # s2
        [1],        # s1
    ]

    print_poly(calculate_routeid(nodes, o, debug=DEBUG))


if __name__ == '__main__':
    _main()
