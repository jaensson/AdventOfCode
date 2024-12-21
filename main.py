import sys
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
from day_10.main import main as day10
from day_11.main import main as day11
from day_12.main import main as day12
from day_13.main import main as day13
from day_14.main import main as day14
from day_15.main import main as day15
from day_16.main import main as day16
from day_17.main import main as day17
from day_18.main import main as day18
from day_19.main import main as day19
from day_20.main import main as day20
from day_21.main import main as day21

parser = argparse.ArgumentParser()
parser.add_argument("--day", help="day to execute")
args = parser.parse_args()


def main(day: str):
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
        "10": day10,
        "11": day11,
        "12": day12,
        "13": day13,
        "14": day14,
        "15": day15,
        "16": day16,
        "17": day17,
        "18": day18,
        "19": day19,
        "20": day20,
        "21": day21,
    }

    days[day]()


if __name__ == "__main__":
    if args.day:
        main(args.day)
