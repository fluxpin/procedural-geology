#!/usr/bin/python -tt

from __future__ import division

import Image as img
import itertools as it
import random as rand

class Ring(list):
    def __getitem__(self, i):
        return list.__getitem__(self, i % len(self))

def displace(plane, h):
    smooth = 2.0 ** -h
    mid = len(plane) >> 1
    dis = 1.0
    while mid:
        # Diamond
        for y in range(mid, len(plane), mid << 1):
            for x in range(mid, len(plane), mid << 1):
                plane[y][x] = (plane[y - mid][x + mid] +
                               plane[y - mid][x - mid] +
                               plane[y + mid][x + mid] +
                               plane[y + mid][x - mid]) / 4.0
                plane[y][x] += rand.uniform(-dis, dis)
        # Square
        for y in range(0, len(plane), mid):
            for x in range((y + mid) % (mid << 1), len(plane), mid << 1):
                plane[y][x] = (plane[y      ][x + mid] +
                               plane[y - mid][x      ] +
                               plane[y      ][x - mid] +
                               plane[y + mid][x      ]) / 4.0
                plane[y][x] += rand.uniform(-dis, dis)
        mid >>= 1
        dis *= smooth

def normalize(plane):
    dis = max(max(it.chain(*plane)), abs(min(it.chain(*plane))))
    for y in range(0, len(plane)):
        for x in range(0, len(plane)):
            plane[y][x] += dis
            plane[y][x] /= dis * 2.0

# res = 2^n
# h is smoothing
def midpoint_displace(res, h):
    plane = Ring(Ring(r) for r in [[0.0] * res] * res)
    displace(plane, h)
    normalize(plane)
    return plane

def main():
    res = 256
    h = 1.0

    plane = midpoint_displace(res, h)
    terrain = img.new('L', (res + 1, res + 1))

    for x in range(0, res + 1):
        for y in range(0, res + 1):
            terrain.putpixel((x, y), int(plane[y][x] * 255))
    terrain.save('terrain2.bmp')

if __name__ == '__main__':
    main()
