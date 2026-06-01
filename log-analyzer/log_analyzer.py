import argparse
import json
import csv
from datetime import datetime


def parse_log_line(line):
    """
    Parse a log line that may be JSON or plain text.

    Plain text format:
    2024-01-15 10:03:22 ERROR Database timeout

    JSON format:
    {"timestamp":"2024-01-15 10:03:22","level":"ERROR","message":"Database timeout"}
    """

    line = line.strip()

    if not line:
        return None

    # Try JSON first
    try:
        data = json.loads(line)

        return {
            "timestamp": data["timestamp"],
            "level": data["level"].upper(),
            "message": data["message"]
        }

    except json.JSONDecodeError:
        pass

    # Plain text format
    parts = line.split(" ", 3)

    if len(parts) < 4:
        return None

    return {
        "timestamp": f"{parts[0]} {parts[1]}",
        "level": parts[2].upper(),
        "message": parts[3]
    }


def parse_timestamp(timestamp):
    """Convert string timestamp into datetime object."""
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")


def export_summary_to_csv(
    filename,
    total_logs,
    errors,
    warnings,
    info,
    most_common_error
):
    """Export analysis summary to CSV."""

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["metric", "value"])
        writer.writerow(["total_logs", total_logs])
        writer.writerow(["errors", errors])
        writer.writerow(["warnings", warnings])
        writer.writerow(["info", info])
        writer.writerow(["most_common_error", most_common_error or "None"])


def main():

    parser = argparse.ArgumentParser(
        description="Log Analyzer CLI"
    )

    parser.add_argument(
        "-file",
        required=True,
        help="Path to log file"
    )

    parser.add_argument(
        "--level",
        choices=["ERROR", "WARNING", "INFO"],
        help="Filter by log level"
    )

    parser.add_argument(
        "--from",
        dest="from_time",
        help="Start timestamp (YYYY-MM-DD HH:MM:SS)"
    )

    parser.add_argument(
        "--to",
        dest="to_time",
        help="End timestamp (YYYY-MM-DD HH:MM:SS)"
    )

    parser.add_argument(
        "-export",
        help="Export summary to CSV"
    )

    args = parser.parse_args()

    total_logs = 0
    errors = 0
    warnings = 0
    info = 0

    error_messages = {}
    failure_timestamps = []

    from_time = (
        parse_timestamp(args.from_time)
        if args.from_time
        else None
    )

    to_time = (
        parse_timestamp(args.to_time)
        if args.to_time
        else None
    )

    try:
        with open(args.file, "r", encoding="utf-8") as file:

            for line in file:

                log = parse_log_line(line)

                if log is None:
                    continue

                log_timestamp = parse_timestamp(
                    log["timestamp"]
                )

                # Level filter
                if args.level and log["level"] != args.level:
                    continue

                # Start time filter
                if from_time and log_timestamp < from_time:
                    continue

                # End time filter
                if to_time and log_timestamp > to_time:
                    continue

                total_logs += 1

                level = log["level"]
                message = log["message"]

                if level == "ERROR":
                    errors += 1

                    failure_timestamps.append(
                        log["timestamp"]
                    )

                    error_messages[message] = (
                        error_messages.get(message, 0) + 1
                    )

                elif level == "WARNING":
                    warnings += 1

                elif level == "INFO":
                    info += 1

    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        return

    except Exception as error:
        print(f"Unexpected error: {error}")
        return

    most_common_error = None

    if error_messages:
        most_common_error = max(
            error_messages,
            key=error_messages.get
        )

    print("\n===== LOG ANALYSIS SUMMARY =====")
    print(f"Total logs:           {total_logs}")
    print(f"Errors:               {errors}")
    print(f"Warnings:             {warnings}")
    print(f"Info:                 {info}")
    print(
        f'Most frequent error:  "{most_common_error}"'
        if most_common_error
        else "Most frequent error:  None"
    )

    print(
        "Failure timestamps:   "
        + (
            ", ".join(failure_timestamps)
            if failure_timestamps
            else "None"
        )
    )

    if args.export:

        export_summary_to_csv(
            args.export,
            total_logs,
            errors,
            warnings,
            info,
            most_common_error
        )

        print(f"\nSummary exported to: {args.export}")


if __name__ == "__main__":
    main()