#!/usr/bin/env python3

from sys import argv

with open(argv[1], "r") as src:
    with open(argv[2], "w") as dst:
        lines = src.readlines()

        imgs = [l for l in lines if l.startswith("i ")]
        
        for l in lines:
            dst.write(l)
            if l == imgs[-1]:
                dst.write(imgs[0])
