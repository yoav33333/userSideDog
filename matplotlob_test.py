
import matplotlib
matplotlib.use('TkAgg')  # Add this line if running in PyCharm

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

L1 = L2 = 90

def inverse_kinematics(x, y):
    d = np.hypot(x, y)
    if d > L1 + L2 or d < abs(L1 - L2):
        return None, None
    cos_theta2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    sin_theta2 = np.sqrt(1 - cos_theta2**2)
    theta2 = np.arctan2(sin_theta2, cos_theta2)
    k1 = L1 + L2 * cos_theta2
    k2 = L2 * sin_theta2
    theta1 = np.arctan2(y, x) - np.arctan2(k2, k1)
    return theta1, theta2

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)

ax_x = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_y = plt.axes([0.25, 0.1, 0.65, 0.03])
slider_x = Slider(ax_x, 'X Target', -180, 180, valinit=-90)
slider_y = Slider(ax_y, 'Y Target', -180, 180, valinit=-90)

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
    t1, t2 = inverse_kinematics(x, y)
    plot_arm(t1, t2, ax)
    fig.canvas.draw_idle()

slider_x.on_changed(update)
slider_y.on_changed(update)

update(None)
plt.show()
