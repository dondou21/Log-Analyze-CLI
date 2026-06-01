import argparse

parser = argparse.ArgumentParser(description="Analyze log files")
parser.add_argument("-file", required=True, help="Path to log file")

args = parser.parse_args()

with open(args.file, "r") as file:
    for index, line in enumerate(file, start=1):
        print(f"Line {index}: {line.strip()}")