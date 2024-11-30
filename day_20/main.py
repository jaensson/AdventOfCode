import os
from typing import List
from enum import Enum


class File(Enum):
    READ = "r"


def read_file(file: str) -> List[str]:
    file = open(file, File.READ.value, encoding="UTF-8")
    lines = file.read()
    # lines = [line for line in file.readlines()]
    lines = lines.split("\n")

    file.close()

    return lines


def main():
    input_file = f"{os.path.dirname(os.path.realpath(__file__))}/input.txt"
    lines = read_file(input_file)

    part1_result = part1(lines)
    print(part1_result)
    part2_result = part2(lines)
    print(part2_result)


def decode_input(lines):
    modules = dict()

    for line in lines:
        destinations = line.split("->")[1].replace(" ", "").split(",")
        for destination in destinations:
            if destination not in modules:
                modules[destination] = {"state": "low"}
        if line.startswith("broadcaster"):
            modules["broadcaster"] = {"destination": destinations}
        else:
            module = line.split("->")[0].strip()
            type, name = module[:1], module[1:]

            modules[name] = {
                "destination": destinations,
                "type": type,
                "state": "off" if type == "%" else "low",
            }
            if type == "&":
                modules[name]["input"] = dict()

    for key, values in modules.items():
        if "destination" not in values:
            continue
        for destination in values["destination"]:
            if (
                "type" in modules[destination]
                and modules[destination]["type"] == "&"
            ):
                modules[destination]["input"][key] = "low"

    return modules


def part1(lines):
    PRESS = 1000
    modules = decode_input(lines)
    queue = []

    pulses = dict({"low": 0, "high": 0, "press": 0})

    while len(queue) != 0 or pulses["press"] != PRESS:
        if len(queue) == 0:
            destinations = [
                ("broadcaster", destination, "low")
                for destination in modules["broadcaster"]["destination"]
            ]

            queue.extend(destinations)
            pulses["press"] += 1
            pulses["low"] += 1

        sender, current_module_name, current_pulse = queue.pop(0)
        current_module = modules[current_module_name]
        pulses[current_pulse] += 1

        if "type" in current_module and current_module["type"] == "%":
            if current_pulse == "low":
                current_state = (
                    "on" if current_module["state"] == "off" else "off"
                )
                pulse = "high" if current_state == "on" else "low"
                current_module["state"] = current_state

                destinations = [
                    (current_module_name, destination, pulse)
                    for destination in current_module["destination"]
                ]
                queue.extend(destinations)

        if "type" in current_module and current_module["type"] == "&":
            current_module["input"][sender] = current_pulse
            pulse = (
                "low"
                if len(
                    [
                        (key, destination)
                        for key, destination in current_module["input"].items()
                        if destination == "high"
                    ]
                )
                == len(current_module["input"])
                else "high"
            )

            destinations = [
                (current_module_name, destination, pulse)
                for destination in current_module["destination"]
            ]
            queue.extend(destinations)

    return pulses["high"] * pulses["low"]


def part2(lines):
    pass


if __name__ == "__main__":
    main()


"""
Använd en QUEUE

Modules skickar pulsar antingen hög eller låg till alla dess destinationsmoduler.

Flip-flop (%) 
- En toggle mellan av/på, default av.
- En inkommande hög puls ignoreras.
- En inkommande låg puls flippar mellan av/på:
    - Om den sätts på skickas en hög puls
    - Om den stängs av skickas en låg puls

Conjuction (&)
- Sparar den senaste inkommande pulsen från alla dess inkommande moduler, default låg.
- Uppdaterar signalen från den inkommande modulen.
- Om alla inkommande moduler är höga skickas en låg puls annars en hög puls.
- Agerar som en inverter om det endast finns en inkommande modul.

Broadcaster
- Skickar den inkommande pulsen till alla dess destinationsmoduler.

Button
- Skickar en låg puls till alla dess destinationsmoduler.

"""
