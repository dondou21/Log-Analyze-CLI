# Project 1 - Log Analyze CLI

<aside>

💡 About the project
A Python CLI that reads a log file and gives you a clean summary - errors, warnings, most common failure, and when it all happened.

 The tool reads a log file line by line and extracts three things from each entry: the log level (ERROR, WARNING, INFO), the message, and the timestamp. Once it has that data, it counts how many of each level exist, finds which error message appeared most often, and collects the timestamps of every failure.

It must handle two log formats, plain text (like Apache or app logs) and JSON structured logs, so the parsing logic needs to detect which format it's dealing with and handle each correctly.

The tool also needs to support filtering. If you only care about errors, you pass `--level ERROR` and it shows only those. If you want to narrow down to a specific window of time, you pass `--from` and `--to` with timestamps. Finally, it should be able to export the summary to a CSV file for sharing or further analysis.

Build it as 6 small features, not one big problem.

</aside>

### Feature-1: Read the log file

**Goal:** Open a log file and read it line by line.

**What to do:**

- Accept a file path via `-file app.log`
- Open the file and read it line by line
- Store or process each line in a loop

**Expected result:**

```
Line 1: 2024-01-15 10:03:22 ERROR Database timeout
Line 2: 2024-01-15 10:04:01 INFO  Server started
...
```

### Feature-2: Detect log format

**Goal:** Figure out if a log line is plain text or JSON and extract the right fields from each.

**Two formats to handle:**

```
2024-01-15 10:03:22 ERROR Database timeout
```

```json
{"timestamp": "...", "level": "ERROR", "message": "Database timeout"}
```

**What to do:**

- Try parsing each line as JSON first
- If it fails, treat the line as plain text
- Extract three fields from each: `timestamp`, `level`, `message`

### Feature-3: Count log levels

**Goal:** Count how many ERROR, WARNING, and INFO entries exist.

**What to do:**

- Initialize counters: `errors = 0`, `warnings = 0`, `info = 0`
- Increment the right counter for each line

**Expected result:**

```
Errors:    45
Warnings: 102
Info:    1053
```

### Feature-4: Find most common error

**Goal:** Find which error message appears the most.

**What to do:**

- Store error messages in a dict: `{"Database timeout": 10, "Auth failed": 5}`
- Increment the count each time the same message appears
- Find the key with the highest value using `max()`

**Expected result:**

```
Most frequent error: "Database timeout"
```

### Feature-5: Filter logs

**Goal:** Let users filter logs by level and time range when running the script.

**What to support:**

```bash
--level ERROR
--from "2024-01-15 10:00" --to "2024-01-15 12:00"
```

**What to do:**

- Skip lines that don't match the requested level
- Parse timestamps and compare them to the given range
- If no filter is passed, show everything

### Feature-6: Export to CSV

**Goal:** Save the summary to a CSV file.

**What to do:**

- Add an `-export summary.csv` flag
- Write total logs, errors, warnings, info, and most common error to the file

**Expected file output:**

```
metric,value
total_logs,1200
errors,45
warnings,102
info,1053
most_common_error,Database timeout
```

### Final output — what the tool should print

```
Total logs:           1200
Errors:                 45
Warnings:              102
Info:                 1053
Most frequent error:  "Database timeout"
Failure timestamps:   10:03:22, 10:07:44, 10:15:01 ...
```