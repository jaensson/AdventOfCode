import argparse
from template.main import main as template
from day_1.main import main as day1
from day_2.main import main as day2

parser = argparse.ArgumentParser()
parser.add_argument("--day", help="day to execute")
args = parser.parse_args()


def main(day: int):
    days = {
        "0": template,
        "1": day1,
        "2": day2,
    }

    days[day]()


if __name__ == "__main__":
    if args.day:
        main(args.day)
