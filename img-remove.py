#!/usr/bin/env python3

from sys import argv

with open(argv[1], "r") as src:
    with open(argv[2], "w") as dst:
        lines = src.readlines()

        imgs = [l for l in lines if l.startswith("i ")]
        num_imgs = len(imgs) - 1
        cp_wrap_src = f"c n{num_imgs-1} N{num_imgs}"
        cp_wrap_dst = f"c n{num_imgs-1} N0"

        first_img = True

        for l in lines:
            if not first_img and l == imgs[-1]:
                continue
            if l.startswith("i "):
                first_img = False
            if l.startswith(cp_wrap_src):
                l = l.replace(cp_wrap_src, cp_wrap_dst)
            dst.write(l)
