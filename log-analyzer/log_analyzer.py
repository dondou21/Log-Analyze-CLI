import argparse
import json
from datetime import datetime

def parse_log_line(line):
    line = line.strip()

    try:
        data = json.loads(line)
        return {
            "timestamp": data["timestamp"],
            "level": data["level"],
            "message": data["message"]
        }
    except json.JSONDecodeError:
        parts = line.split(" ", 3)

        if len(parts) < 4:
            return None

        return {
            "timestamp": f"{parts[0]} {parts[1]}",
            "level": parts[2],
            "message": parts[3]
        }


parser = argparse.ArgumentParser(description="Analyze log files")
parser.add_argument("-file", required=True, help="Path to log file")

args = parser.parse_args()

with open(args.file, "r") as file:
    for line in file:
        log = parse_log_line(line)
        print(log)