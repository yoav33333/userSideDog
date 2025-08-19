import asyncio
import math
from time import sleep

import numpy as np

from robot import send_poses, inverse_kinematics, send_xy

import math
import time


def generate_path(center, radius, line_length, steps_per_segment=20 , speed=1.0):
    cx, cy = center

    # Path 1: flat line (rightward)
    line_points = []
    for i in range(steps_per_segment):
        t = i / (steps_per_segment - 1)
        x = cx - line_length / 2 + t * line_length
        y = cy
        line_points.append((x, y))

    # Path 2: half circle (from right end back to start)
    half_circle_points = []
    for i in range(int(steps_per_segment*math.pi/2)):
        theta = math.pi * (i / (int(steps_per_segment*math.pi/2) - 1))  # 0 to pi
        x = cx - radius * math.cos(theta)
        y = cy - radius * math.sin(theta)
        half_circle_points.append((x, y))
    half_circle_points = half_circle_points[::-1]  # Reverse to go from right to left
    # Combine paths
    path = line_points + half_circle_points
    return path


# Example usage: generate positions for a full circle
if __name__ == "__main__":
    center = (100, 0)
    radius = 40
    path = generate_path(radius=radius, line_length=radius*2, center=center)
    while True:
        for pos in path:
            # pos = circle_position(center[0], center[1], radius, angle)
            asyncio.run(send_xy(*pos))

            print(f"x={pos[1]:.2f}, y={pos[0]:.2f}")
