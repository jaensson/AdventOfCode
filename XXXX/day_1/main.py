import os
import sys
from lib.helpers import read_file

CURRENT_DIRNAME = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CURRENT_DIRNAME + "../../../")


def main():
    global CURRENT_DIRNAME
    input_file = f"{CURRENT_DIRNAME}/input.txt"
    lines = read_file(input_file)
    print(lines)


if __name__ == "__main__":
    main()
