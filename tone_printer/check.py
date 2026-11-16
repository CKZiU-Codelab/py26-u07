#!/usr/bin/env python3
"""Self-check for the project "Tone Printer" (u07).

Run it in the project directory:

    python3 check.py

The script reads only the files your program produced. It never runs
your program, so generate the files first, then check them. Each
[fail] line names one requirement; fix it and run the script again.
"""

import csv
import html as html_lib
import os
import re
import sys


class Fail(Exception):
    pass


CHECKS = []
WARNINGS = []


def check(name):
    def register(function):
        CHECKS.append((name, function))
        return function
    return register


def warn(message):
    WARNINGS.append(message)


def read_text(path):
    if not os.path.exists(path):
        raise Fail("%s is missing" % path)
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def read_csv(path):
    if not os.path.exists(path):
        raise Fail("%s is missing" % path)
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise Fail("%s is empty" % path)
    return rows


def require_files(*names):
    missing = [name for name in names if not os.path.exists(name)]
    if missing:
        raise Fail("missing: %s" % ", ".join(missing))


def require_notes(*headings):
    text = read_text("notes.md")
    missing = [heading for heading in headings if heading not in text]
    if missing:
        raise Fail("notes.md has no section: %s" % " | ".join(missing))


def read_pnm(path):
    text = read_text(path)
    lines = [line.split("#")[0] for line in text.splitlines()]
    tokens = " ".join(lines).split()
    if not tokens:
        raise Fail("%s is empty" % path)
    magic = tokens[0]
    if magic not in ("P1", "P2", "P3"):
        raise Fail("%s starts with %r; use the text formats P1, P2 or P3" % (path, magic))
    try:
        width = int(tokens[1])
        height = int(tokens[2])
    except (IndexError, ValueError):
        raise Fail("%s: the width and the height are missing from the header" % path)
    index = 3
    maxval = 1
    if magic in ("P2", "P3"):
        try:
            maxval = int(tokens[3])
        except (IndexError, ValueError):
            raise Fail("%s: the maximum value is missing from the header" % path)
        index = 4
    channels = 3 if magic == "P3" else 1
    needed = width * height * channels
    values = tokens[index:]
    if len(values) != needed:
        raise Fail("%s: the header says %dx%d, which needs %d values, but the file has %d"
                   % (path, width, height, needed, len(values)))
    try:
        numbers = [int(value) for value in values]
    except ValueError:
        raise Fail("%s contains a value that is not an integer" % path)
    for number in numbers:
        if number < 0 or number > maxval:
            raise Fail("%s has the value %d, outside 0..%d" % (path, number, maxval))
    return {"magic": magic, "width": width, "height": height,
            "maxval": maxval, "values": numbers, "path": path}


def find_frames(minimum=8):
    if not os.path.isdir("frames"):
        raise Fail("the frames/ directory is missing")
    names = sorted(name for name in os.listdir("frames") if name.endswith(".pgm"))
    if not names:
        raise Fail("frames/ has no .pgm files")
    bad = [name for name in names if not re.match(r"^frame_\d\d\.pgm$", name)]
    if bad:
        raise Fail("these names do not use two digits: %s" % ", ".join(bad[:3]))
    if len(names) < minimum:
        raise Fail("only %d frames; the animation needs at least %d" % (len(names), minimum))
    return ["frames/" + name for name in names]


def numbers_in(text):
    return [float(value) for value in re.findall(r"-?\d+(?:\.\d+)?", text)]


def require_gif(path):
    if not os.path.exists(path):
        raise Fail("%s is missing; build it with the convert command from the brief" % path)
    with open(path, "rb") as handle:
        head = handle.read(6)
    if not head.startswith(b"GIF8"):
        raise Fail("%s does not start with GIF8; is it really a GIF?" % path)


def scan_sources(forbidden):
    for name in sorted(os.listdir(".")):
        if not name.endswith(".py") or name == "check.py":
            continue
        with open(name, encoding="utf-8") as handle:
            for number, line in enumerate(handle, start=1):
                code = line.split("#")[0]
                for token in forbidden:
                    if token in code:
                        warn("%s:%d uses %s; the brief asks for a different tool."
                             % (name, number, token))


def main():
    print("")
    print("Checking the project in %s" % os.getcwd())
    print("")
    passed = 0
    failed = 0
    for name, function in CHECKS:
        try:
            function()
        except Fail as error:
            failed += 1
            print("[fail] %s" % name)
            print("       %s" % error)
        except Exception as error:
            failed += 1
            print("[fail] %s" % name)
            print("       the check itself stopped: %s: %s" % (type(error).__name__, error))
        else:
            passed += 1
            print("[ok]   %s" % name)
    print("")
    for message in WARNINGS:
        print("[warn] %s" % message)
    if WARNINGS:
        print("")
    print("%d passed, %d failed" % (passed, failed))
    if failed:
        print("NOT READY YET - fix the [fail] lines above and run the script again.")
        return 1
    print("PROJECT READY - every automatic check passed. Show the program and notes.md.")
    return 0



@check("the files named in the brief exist")
def files():
    require_files("wave_lab.py", "tone.py", "wave_440_sine.pgm", "tone_440_square.pgm",
                  "tone_440_triangle.pgm", "octave.pgm", "tuning.csv", "wave.gif", "notes.md")


@check("tuning.csv has thirteen notes and A4 is 440.00 Hz")
def tuning():
    rows = read_csv("tuning.csv")
    header = [cell.strip().lower() for cell in rows[0]]
    if header != ["note", "semitones", "frequency"]:
        raise Fail("tuning.csv header is %s; expected note,semitones,frequency"
                   % ",".join(header))
    if len(rows) - 1 != 13:
        raise Fail("tuning.csv has %d notes; one octave has thirteen" % (len(rows) - 1))
    for number, row in enumerate(rows[1:], start=2):
        if len(row) != 3:
            raise Fail("line %d of tuning.csv has %d cells, three expected"
                       % (number, len(row)))
    return rows


@check("every note is 2 ** (1 / 12) above the one before it")
def octave():
    rows = tuning()
    data = []
    for number, row in enumerate(rows[1:], start=2):
        try:
            semitones = int(row[1])
            frequency = float(row[2])
        except ValueError:
            raise Fail("line %d of tuning.csv is not numeric" % number)
        data.append((row[0].strip(), semitones, frequency))
    data.sort(key=lambda item: item[1])
    found = [frequency for name, semitones, frequency in data if semitones == 0]
    if not found:
        raise Fail("tuning.csv has no row with 0 semitones (A4)")
    if abs(found[0] - 440.0) > 0.01:
        raise Fail("A4 is %.2f Hz; it must be 440.00" % found[0])
    step = 2 ** (1.0 / 12.0)
    for first, second in zip(data, data[1:]):
        if second[1] - first[1] != 1:
            raise Fail("the semitone column jumps from %d to %d" % (first[1], second[1]))
        expected = first[2] * step
        if abs(second[2] - expected) > expected * 0.005:
            raise Fail("%s is %.2f Hz, expected about %.2f" % (second[0], second[2], expected))


@check("the PGM files are valid and use the maximum value 255")
def pictures():
    for name in ("wave_440_sine.pgm", "tone_440_square.pgm",
                 "tone_440_triangle.pgm", "octave.pgm"):
        image = read_pnm(name)
        if image["magic"] != "P2":
            raise Fail("%s is %s; the pictures use the PGM format P2" % (name, image["magic"]))
        if image["maxval"] != 255:
            raise Fail("%s has the maximum value %d; the brief uses 255"
                       % (name, image["maxval"]))


@check("frames/ holds at least eight frames and wave.gif is a GIF")
def animation():
    paths = find_frames()
    sizes = []
    for path in paths:
        image = read_pnm(path)
        sizes.append((image["width"], image["height"]))
    if len(set(sizes)) != 1:
        raise Fail("the frames do not all have the same size: %s" % sorted(set(sizes)))
    require_gif("wave.gif")


@check("notes.md has the four notes from the brief")
def notes():
    require_notes("## The New Thing – a function from a module",
                  "## The New Thing – rounding to a pixel",
                  "## Milestone 3 – clipping or scaling",
                  "## Milestone 6 – reading the picture back")

if __name__ == "__main__":
    sys.exit(main())
