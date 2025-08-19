import asyncio
import math
from time import sleep

import numpy as np
import websockets

L1 = L2 = 90  # Lengths of the two links in mm

def inverse_kinematics(x, y):
    d = np.hypot(x, y)
    temp = x
    x = y
    y = temp
    if d > L1 + L2 or d < abs(L1 - L2):
        return None, None
    cos_angle2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    angle2 = np.arccos(np.clip(cos_angle2, -1.0, 1.0))
    k1 = L1 + L2 * np.cos(angle2)
    k2 = L2 * np.sin(angle2)
    angle1 = np.arctan2(y, x) - np.arctan2(k2, k1)
    return angle1, angle2
async def send_xy(x, y):
    uri = "ws://10.10.0.46:8765"
    async with websockets.connect(uri) as websocket:
        msg = f"{x},{y}"
        await websocket.send(msg)
        print(f"Sent: {msg}")
async def send_poses(t1, t2):
    uri = "ws://10.10.0.46:8765"
    async with websockets.connect(uri) as websocket:
        msg = f"{np.degrees(t1+math.pi/2)},{np.degrees(t2+t1)}"
        await websocket.send(msg)
        print(f"Sent: {msg}")

# asyncio.run(send_xy(15, 90))
# sleep(1)