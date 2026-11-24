#!/usr/bin/env python3
"""One-Liner Marathon — writes one original comedy line to /output/entry.txt.

The joke is a single line of at most 280 characters. The program checks the
line first (length, single line, no stray whitespace) and writes it atomically,
so a reader never sees a half-written file.
"""

import os
import sys

JOKE = "My bank emailed me 'we miss you' — bold, from an institution that charges me $12 a month to keep my own money in a building that closes on Sundays."

MAX_CHARS = 280
OUTPUT_PATH = "/output/entry.txt"


def check_line(line):
    """Return a list of problems with the line; empty means it is fine."""
    problems = []
    if not line.strip():
        problems.append("line is empty or only whitespace")
    if len(line) > MAX_CHARS:
        problems.append(
            "line is %d characters, over the %d limit" % (len(line), MAX_CHARS)
        )
    if "\n" in line.strip():
        problems.append("line spans more than one line")
    if line != line.strip():
        problems.append("line has leading or trailing whitespace")
    return problems


def write_line(line, path):
    """Write the line atomically: temp file in the same folder, then rename."""
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        handle.write(line)
    os.replace(tmp, path)


def verify_written(line, path):
    """Read the file back and confirm it holds exactly the line we wrote."""
    with open(path, "r", encoding="utf-8") as handle:
        back = handle.read()
    if back != line:
        return "wrote %d characters but read back %d" % (len(line), len(back))
    return None


def main():
    problems = check_line(JOKE)
    if problems:
        for problem in problems:
            print("bad line: " + problem, file=sys.stderr)
        return 1
    write_line(JOKE, OUTPUT_PATH)
    mismatch = verify_written(JOKE, OUTPUT_PATH)
    if mismatch:
        print("bad write: " + mismatch, file=sys.stderr)
        return 1
    print("wrote %d characters to %s" % (len(JOKE), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
