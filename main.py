import argparse
from template.main import main as template
from day_1.main import main as day1
from day_2.main import main as day2
from day_3.main import main as day3
from day_4.main import main as day4
from day_5.main import main as day5
from day_6.main import main as day6
from day_7.main import main as day7
from day_8.main import main as day8
from day_9.main import main as day9

parser = argparse.ArgumentParser()
parser.add_argument("--day", help="day to execute")
args = parser.parse_args()


def main(day: int):
    days = {
        "0": template,
        "1": day1,
        "2": day2,
        "3": day3,
        "4": day4,
        "5": day5,
        "6": day6,
        "7": day7,
        "8": day8,
        "9": day9,
    }

    days[day]()


if __name__ == "__main__":
    if args.day:
        main(args.day)
