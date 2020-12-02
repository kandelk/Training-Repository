import time

import matplotlib.pyplot as plt
import numpy as np


def create_and_save_hbar(xval, yval, folder):
    fig, ax = plt.subplots()
    position = np.arange(len(yval))

    ax.barh(position, xval)

    ax.set_yticks(position)
    ax.set_yticklabels(yval)

    fig.savefig(f"{folder}/{time.time()}.png")
