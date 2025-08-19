import asyncio
from time import sleep

from robot import send_xy

while True:
    try:
        asyncio.run(send_xy(90,90))
    except:
        pass
    sleep(0.5)