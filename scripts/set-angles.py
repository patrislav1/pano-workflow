#!/usr/bin/env python3

import re
import sys
import argparse

RE_PTOPARSE = re.compile(r"^([a-zA-Z]+)(=?[\-0-9\.]+)")

def pto_parse(fname):
    l = open(fname, "r").readlines()

    imgs = []
    for idx, line in enumerate(l):
        if not line.startswith("i "):
            continue

        properties_str = [ls.strip() for ls in line.split(" ")]
        properties = {}

        for p in properties_str:
            if p.startswith("n"):
                properties["n"] = p[1:]
                continue

            m = RE_PTOPARSE.match(p)
            if not m:
                continue
            properties[m.group(1)] = m.group(2)

        imgs.append({
            "idx": idx,
            "properties": properties
        })
    return l, imgs


def pto_write(fname, lines, imgs):
    for img in imgs:
        lines[img["idx"]] = " ".join(
            ["i "] + [f"{k}{v}" for k, v in img["properties"].items()]
        ) + "\n"
    with open(fname, "w") as f:
        f.writelines(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Set angles for images in PTO project'
    )
    parser.add_argument('srcfile',
                        type=str,
                        help='Source file for reading'
                        )
    parser.add_argument('-o', '--output',
                        type=str,
                        help='output file'
                        )
    parser.add_argument('-s', '--slant-angle',
                        type=float,
                        help='slant angle of nodal point adapter'
                        )
    parser.add_argument('-c', '--counterclockwise',
                        action='store_true',
                        help='assume counterclockwise rotation instead of clockwise'
                        )

    args = parser.parse_args()

    lines, imgs = pto_parse(args.srcfile)
    num_pos = len(imgs)

    slant_angle = args.slant_angle or 0.0
    yaw_increment = 360 / num_pos
    if args.counterclockwise:
        yaw_increment = -yaw_increment

    print(f"Detected {len(imgs)} images, increment of {yaw_increment}")

    yaw_angle = 0
    for i in imgs:
        i["properties"]["r"] = str(-slant_angle % 360)
        i["properties"]["y"] = str(yaw_angle % 360)
        yaw_angle += yaw_increment

    outfile = args.output if args.output else args.srcfile
    pto_write(outfile, lines, imgs)


if __name__ == "__main__":
    main()

