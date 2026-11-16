# Project – Tone Printer

**Individual Project Brief – Week 6 · u07**

Start: Monday, 16 November 2026. Show the working program on Monday, 23 November 2026.

## The Idea

You build a program that draws sound. It computes the samples of a tone, scales them to brightness values, and writes the waveform as a PGM picture: time runs to the right, amplitude goes up and down. It can draw a sine, a square and a triangle, in any frequency and amplitude you type in. Then it shifts the phase a few times and `convert` joins the frames into a GIF of a wave travelling across the picture. A second output is a CSV file with the frequencies of one octave, computed from A4 = 440 Hz.

The picture is not a recording. It is a formula turned into pixels — the same formula that is inside every synthesiser, and the same three lines of arithmetic that connect physics, music and code.

## Why This Project Is Yours

You listen to classical music, you finished a woodworking course, and you are interested in physics and in current — a breadboard and a soldering iron are not exotic objects for you. A waveform is where those worlds meet: a physical quantity, sampled at regular intervals, stored as numbers, drawn as a picture. Woodworking also taught you something this project needs: measure twice, cut once. Here the measurement is the period of the wave in samples, and cutting it wrong is visible immediately.

## What You Already Have

- Lists, tuples, slices, `for` loops, nested loops and conditions.
- Arithmetic operators including `//`, `%` and comparisons, and `%s`, `%d`, `%.2f` formatting.
- Files inside `with`, the `csv` module, and the PGM format with its `P2` header and maximum value.
- Terminal work and `git` from the first weeks.

## The New Thing

A wave is a function of time, so this week the language needs mathematics. Find out how to:

1. Import a module and call a function from it, and what `math.pi` is.
2. What `math.sin()` expects as an argument, and what it returns for `0`, `math.pi / 2` and `math.pi`.
3. How to compute the value of a sine at a moment in time when you know the frequency.
4. What `**` does, and how `2 ** (1 / 12)` is used to move one semitone.
5. What `int()` does to `127.9` and what `round()` does to it, and which one you want when you convert a sample to a pixel.
6. What happens when a computed brightness is above the maximum value in the header.

**Write it down:** Create `notes.md` with `## The New Thing – a function from a module`. Explain in three sentences what `math.sin()` takes and returns, with the values for three angles you checked yourself. Add `## The New Thing – rounding to a pixel` with one example where `int()` and `round()` disagree, and one sentence about which one you used and why.

## The Plan

### Milestone 1 – A table of samples

Create `wave_lab.py`.

1. Print a table of ten values of `math.sin()` between `0` and `2 * math.pi`, with the angle and the value, three decimals.
2. Print the same table for a full period of a `440` Hz tone sampled `200` times per second, in milliseconds.
3. Count the samples in one period and print the number.
4. Check your count against `200 / 440` and explain the difference.

At the end of this step you can say how many samples one period of A4 takes at that sample rate.

### Milestone 2 – From samples to a picture

1. Build a buffer `200` pixels wide and `101` pixels high, every pixel white.
2. Compute a sample for every column, scale it to a row, and set that pixel black.
3. Write `wave.pgm` with a `P2` header and open it.
4. Draw a horizontal line at the zero level in a light gray, so the axis is visible.

At the end of this step the viewer shows one period of a sine wave and a visible axis.

### Milestone 3 – Frequency, amplitude and shape

1. Ask for a frequency, an amplitude from `1` to `100` percent, and a shape: `sine`, `square` or `triangle`.
2. Compute the samples for the shape you chose, with conditions instead of a formula where that is simpler.
3. Write the file with the frequency and the shape in its name, for example `tone_440_sine.pgm`.
4. Compare the three shapes at the same frequency.

At the end of this step three pictures show the same period with three different outlines.

### Milestone 4 – The octave

1. Generate the twelve notes from C4 to B4 using `440 * 2 ** (n / 12)`, where `n` is the number of semitones from A4.
2. Round each frequency to two decimals and write `tuning.csv` with `note,semitones,frequency`.
3. Print the table and check two entries against a tuning table you find yourself.
4. Draw all twelve tones as rows in one picture, `octave.pgm`, so that the periods can be compared by eye.

At the end of this step the picture shows the periods getting shorter from left to right, or from top to bottom.

### Milestone 5 – Frames

1. Draw the same tone eight times, each time with a small phase shift.
2. Write the frames to `frames/frame_01.pgm` … `frames/frame_08.pgm` with `%02d` numbers.
3. Build the animation: `convert -delay 20 -loop 0 frames/frame_*.pgm wave.gif`.
4. Check that the wave travels in one direction and that the loop does not jump.

### Milestone 6 – Read it back

1. Read `wave.pgm` with your own code: skip the header, then collect the numbers of one row.
2. Find the darkest column in every row you read, and print it.
3. Compare that column with the sample you computed for the same time.
4. Write two sentences in `notes.md` about what the comparison proves about your writer and your reader.

## Example

```text
Frequency (Hz): 440
Amplitude (1-100): 80
Shape (sine, square, triangle): sine
Sample rate: 200 per second

Period: 0.4545 s
Samples per period: 90.909 -> 91 columns

wave_440_sine.pgm
  row 50 (axis): ..........#........... (light gray)

tuning.csv
note,semitones,frequency
C4,-9,261.63
C#4,-8,277.18
D4,-7,293.66
...
A4,0,440.00
...
B4,2,493.88

Saved octave.pgm (200x120)
Saved frames/frame_01.pgm ... frames/frame_08.pgm
Saved wave.gif
```

## Requirements

- One program, `tone.py` (plus the lab file `wave_lab.py`), started from the terminal.
- Every sample is computed, never typed in. The only inputs are the numbers you type and the formulas in the code.
- The value written to the file is always inside `0..255`; clipping or scaling is your decision and is explained in `notes.md`.
- `tuning.csv` is written with the `csv` module and its frequencies use `%.2f`.
- Each PGM file has a correct header, one row of numbers per line, and the same width and height as the buffer.
- The GIF is built from at least eight frames with two-digit numbering.
- Reading one file back is part of the program, not a separate experiment you threw away.

## Files

```text
tone_printer/
├── wave_lab.py
├── tone.py
├── wave_440_sine.pgm
├── tone_440_square.pgm
├── tone_440_triangle.pgm
├── octave.pgm
├── tuning.csv
├── frames/
│   ├── frame_01.pgm
│   └── ...
├── wave.gif
├── notes.md
└── check.py
```

Commit the whole directory to your repository and push it before the Monday session. A directory that exists only on your laptop cannot be checked.

Run `python3 check.py` in the project directory before you commit. It reads the files your program produced, not your code, and prints one line per requirement.


## How It Will Be Checked

- The number of columns in one period matches the frequency and the sample rate you declared.
- A higher frequency gives more periods in the same width, and the pictures show it.
- `tuning.csv` has thirteen rows, and the A4 row is `440.00`.
- The frames differ only by phase; nothing else moves.
- The value read back from the file matches the value written for the same column.
- You can explain what `math.sin()` returns for an angle of `math.pi` without running the program.

**Hint:** Compute the sample first, then decide the pixel. One sample becomes one column, and the amplitude decides how far the column is from the middle. Keep the middle row in a variable, so that changing the picture height does not break the drawing.

**Additional challenge:** Add a second tone and draw the sum of the two waves — a chord. Then draw the same sum with the amplitudes of the two tones different, and describe in `notes.md` what changes in the picture and what does not. A guitar player would recognize this as the difference between a fifth and an octave; a physicist would call it superposition.

## Suggested Learning Resources

- [The `math` module – `sin`, `pi`, `isqrt`](https://docs.python.org/3/library/math.html)
- [Floating point arithmetic – why `0.1 + 0.2` is not `0.3`](https://docs.python.org/3/tutorial/floatingpoint.html)
- [The `csv` module – reading and writing tabular data](https://docs.python.org/3/library/csv.html)
- [Netpbm – description of the PGM format](https://netpbm.sourceforge.net/doc/pgm.html)
- [ImageMagick – `convert` and animation](https://imagemagick.org/script/convert.php)

**Final goal:** By the end of this project, you should have a program that turns a physical formula into a picture, compares frequencies as pictures, writes a table of note frequencies, and animates a travelling wave — using loops, conditions, lists, `%` formatting and files from the first five weeks, and a module you researched yourself.
