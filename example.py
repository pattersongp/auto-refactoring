#!/usr/bin/env python

from data import Point


def make_point(x: int = 0, y: int = 0) -> Point:
    point: Point = Point(x=x, y=y)
    print(f"made Point {point.x=} {point.y=}")
    return point


if __name__ == "__main__":

    point: Point = make_point(1, 2)
    x = point.x
    y = point.y

    zz = {"hello": "world", "asdf": x}
