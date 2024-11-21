import sys
from template.main import main as template
from day_1.main import main as day1


def main(day: int):
    if day == "0":
        template()
    elif day == "1":
        day1()


if __name__ == "__main__":
    day = sys.argv[1]
    main(day)
