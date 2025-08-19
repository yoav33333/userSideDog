import asyncio
import math
from time import sleep

import matplotlib
import websockets
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

from robot import inverse_kinematics, send_poses, send_xy

matplotlib.use('TkAgg')  # Add this line if running in PyCharm

# Arm lengths
L1 = L2 = 90




fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
ax_x = plt.axes([0.15, 0.1, 0.7, 0.03])
ax_y = plt.axes([0.15, 0.05, 0.7, 0.03])
slider_x = Slider(ax_x, 'X', 0, 179, valinit=90)
slider_y = Slider(ax_y, 'Y', 0, 179, valinit=90)



def plot_arm(theta1, theta2, ax):
    ax.clear()
    if theta1 is None or theta2 is None:
        ax.text(0, 0, "Target out of reach", ha="center", va="center", fontsize=12, color="red")
        ax.set_xlim(-200, 200)
        ax.set_ylim(-200, 200)
        ax.set_aspect('equal')
        ax.grid(True)
        return
    x0, y0 = 0, 0
    x1 = L1 * np.cos(theta1)
    y1 = L1 * np.sin(theta1)
    x2 = x1 + L2 * np.cos(theta1 + theta2)
    y2 = y1 + L2 * np.sin(theta1 + theta2)
    ax.plot([x0, x1, x2], [y0, y1, y2], 'b-o', linewidth=3)
    ax.scatter([x0, x1, x2], [y0, y1, y2], color='red', zorder=5)

    # Visualize theta1 at base (relative to Y axis)
    arc1 = matplotlib.patches.Arc((x0, y0), 40, 40, angle=0,
                                  theta1=0, theta2=np.degrees(theta1),
                                  color='green', lw=2)
    ax.add_patch(arc1)
    ax.text(30 * np.cos(theta1 / 2), 30 * np.sin(theta1 / 2),
            f'{np.degrees(theta1+math.pi/2):.1f}°', color='green', fontsize=10)

    # Visualize absolute angle of second link (relative to Y axis)
    abs_angle2 = theta1 + theta2
    # Arc from Y axis (vertical) to second link
    arc2 = matplotlib.patches.Arc((x1, y1), 30, 30, angle=0,
                                  theta1=0, theta2=np.degrees(abs_angle2),
                                  color='purple', lw=2)
    ax.add_patch(arc2)
    ax.text(x1 + 20 * np.cos(abs_angle2 / 2), y1 + 20 * np.sin(abs_angle2 / 2),
            f'{np.degrees(abs_angle2):.1f}°', color='purple', fontsize=10)

    ax.set_xlim(-200, 200)
    ax.set_ylim(-200, 200)
    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_title("2-Link Arm with Sliders")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

def update(val):
    x = slider_x.val
    y = slider_y.val
    asyncio.run(send_xy(x, y))
    theta1, theta2 = inverse_kinematics(x, y)
    print("Inverse Kinematics -> Theta1: {:.2f}, Theta2: {:.2f}".format(np.degrees(theta1+math.pi/2), np.degrees(theta2+theta1)))
    plot_arm(theta1, theta2, ax)
    fig.canvas.draw_idle()

slider_x.on_changed(update)
slider_y.on_changed(update)
update(None)
plt.show()