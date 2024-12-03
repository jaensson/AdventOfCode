import sys
from template.main import main as template
from day_1.main import main as day1
from day_2.main import main as day2
from day_3.main import main as day3


def main(day: int):
    match day:
        case "0":
            template()
        case "1":
            day1()
        case "2":
            day2()
        case "3":
            day3()


if __name__ == "__main__":
    day = sys.argv[1]
    main(day)
