"""A single python list append happens too fast to measure reliably. Can get a more
accurate measurement by performing a series of n appends on initially empty
list and determining average cost of each."""

from time import time

def compute_average(n):
    """Perform n appends to an empty list and return average time elapsed."""
    data = []
    start = time()
    for k in range(n):
        data.append(None)
    end = time()
    return ((end - start) / n)


def main():
    nvals = [10**i for i in range(2, 9)]
    for n in nvals:
        print(compute_average(n))

if __name__ == '__main__':
    main()

# test
# test2
