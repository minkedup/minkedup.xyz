#!/usr/bin/env python3
"""
Convert a custom Nonogram representation to GoAT.
"""

from typing import TypedDict, TextIO, cast
import io
import sys
import json
import argparse
import collections


class SerializedNonogram(TypedDict):
    """
    :m:  Number of Rows
    :n:  Number of Columns
    :vs: Values for each Column/Row; Left to Right; Columns first
    :fs: Fills w/ Coordinates
    """

    m: int
    n: int
    vs: list[list[int]]
    fs: list[tuple[int, int, str]]


def _to_goat(nonogram: SerializedNonogram) -> str:
    buf = io.StringIO()

    prefix: dict[int, dict[int, str]] = collections.defaultdict(dict)

    fs: list[tuple[int, int, str]] = nonogram["fs"] if "fs" in nonogram else []

    for fill in fs:
        assert len(fill) == 3

        i, j, c = fill

        assert isinstance(i, int)
        assert isinstance(j, int)
        assert isinstance(c, str)

        prefix[i][j] = c

    ncols = nonogram["n"]
    nrows = nonogram["m"]

    col_lists = nonogram["vs"][:ncols]
    row_lists = nonogram["vs"][ncols:]

    max_col_list_len = max(map(len, col_lists))
    max_row_list_len = max(map(len, row_lists))

    row_padding_n = 1 + (max_row_list_len * 3)

    first = True

    for s in range(max_col_list_len, 0, -1):
        if first:
            first = False
        else:
            buf.write("\n")

        buf.write(" " * row_padding_n)

        for item in col_lists:
            if len(item) >= s:
                idx = abs(s - len(item))
                buf.write(f"  {item[idx]} ")
            else:
                buf.write("    ")

        buf.write("\n")

    start = (" " * row_padding_n) + ".---" + ("+---" * (ncols - 1)) + ".\n"
    buf.write(start)

    midline = (" " * row_padding_n) + "+---" + ("+---" * (ncols - 1)) + "+\n"

    for i in range(0, nrows):
        buf.write(" ")

        leftover = 3 * (max_row_list_len - len(row_lists[i]))
        buf.write(" " * leftover)

        for n in row_lists[i]:
            buf.write(f"{n}  ")

        buf.write("|")
        for j in range(0, ncols):

            if j in prefix[i]:
                inside = prefix[i][j]
            else:
                inside = " "

            buf.write(f" {inside} |")

        buf.write("\n")
        buf.write(midline)

    buf.seek(0)
    return buf.read()


def main() -> None:
    """
    Parse Arguments.
    """

    parser = argparse.ArgumentParser(prog="nono_to_goat")
    parser.add_argument("-i", "--input", help="input file (default stdin)")
    parser.add_argument("-o", "--output", help="output file (default stdout)")
    args = parser.parse_args()

    infile: TextIO | None = None

    if args.input is not None:
        infile = open(args.input, "r", encoding="utf-8")
    else:
        infile = sys.stdin

    loaded = json.load(infile)
    nonogram = cast(SerializedNonogram, loaded)

    goated = _to_goat(nonogram)

    outfile: TextIO | None = None

    if args.output is not None:
        outfile = open(args.output, "w", encoding="utf-8")
    else:
        outfile = sys.stdout

    outfile.write(goated)


if __name__ == "__main__":
    main()
