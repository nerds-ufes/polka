#!/usr/bin/python3

def test_cml(hdr_cml=0):
    new_cml = (y + poly2) * lpc
    new_cml = (new_cml & mersenne) + (new_cml >> mersenne_b)
    if new_cml > mersenne:
        new_cml = new_cml - mersenne
    new_cml = hdr_cml + new_cml
    hdr_cml = new_cml
    print(f"New CML value: {hdr_cml}")


if __name__ == "__main__":
    print("Testing CML calc")
    x = 5
    y = 7
    lpc = 17
    mersenne = 31
    mersenne_b = 5
    poly2 = 14
    new_cml = 0
    test_cml(hdr_cml=39)
