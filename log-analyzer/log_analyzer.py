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

total_logs = 0
errors = 0
warnings = 0
info = 0
error_messages = {}
failure_timestamps = []

with open(args.file, "r") as file:
    for line in file:
        log = parse_log_line(line)

        if log is None:
            continue

        total_logs += 1

        level = log["level"]
        message = log["message"]
        timestamp = log["timestamp"]

        if level == "ERROR":
            errors += 1
            failure_timestamps.append(timestamp)
            error_messages[message] = error_messages.get(message, 0) + 1

        elif level == "WARNING":
            warnings += 1

        elif level == "INFO":
            info += 1

most_common_error = None

if error_messages:
    most_common_error = max(error_messages, key=error_messages.get)

print(f"Total logs:          {total_logs}")
print(f"Errors:              {errors}")
print(f"Warnings:            {warnings}")
print(f"Info:                {info}")
print(f'Most frequent error: "{most_common_error}"')
print(f"Failure timestamps:  {', '.join(failure_timestamps)}")