#!/usr/bin/python -tt

from __future__ import division

import Image as img
import random as rand

class Ring(list):
    def __getitem__(self, i):
        return list.__getitem__(self, i % len(self))

def displace(line, h):
    smooth = 2.0 ** -h
    mid = len(line) >> 1
    dis = 1.0
    while mid:
        for x in range(mid, len(line), mid << 1):
            line[x] = (line[x - mid] + line[x + mid]) / 2.0
            line[x] += rand.uniform(-dis, dis)
        mid >>= 1
        dis *= smooth

def normalize(line):
    dis = max(max(line), abs(min(line)))
    for x in range(0, len(line)):
        line[x] += dis
        line[x] /= dis * 2.0

# res = 2^n
# h is smoothing
def midpoint_displace(res, h):
    line = Ring([0.0] * res)
    displace(line, h)
    normalize(line)
    return line

def main():
    res = 256
    h = 1.0

    line = midpoint_displace(res, h)
    terrain = img.new('1', (res + 1, res))

    for x in range(0, res + 1):
        for y in range(0, int(line[x] * res)):
            terrain.putpixel((x, res - 1 - y), 1)
    terrain.save('terrain1.bmp')

if __name__ == '__main__':
    main()
