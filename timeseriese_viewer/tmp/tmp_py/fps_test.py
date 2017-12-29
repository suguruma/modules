import matplotlib.pyplot as plt
import numpy as np
import time

from scipy.stats._continuous_distns import t_gen


def case1():

    fig, ax = plt.subplots()

    t_start = time.time()
    num_plot = 0

    while time.time() - t_start < 1:
        ax.clear()
        ax.plot(np.random.randn(100))
        plt.pause(0.001)

        num_plot += 1

    return num_plot


def case2():

    fig, ax = plt.subplots()
    line, = ax.plot(np.random.randn(100))

    t_start = time.time()
    num_plot = 0

    while time.time() - t_start < 1:
        line.set_ydata(np.random.randn(100))
        plt.pause(0.001)

        num_plot += 1

    return num_plot


def case3():

    fig, ax = plt.subplots()
    line, = ax.plot(np.random.randn(100))
    fig.canvas.draw()
    fig.show()

    t_start = time.time()
    num_plot = 0

    while time.time() - t_start < 1:
        line.set_ydata(np.random.randn(100))
        fig.canvas.draw()
        fig.canvas.flush_events() # <-これがないと画面に描画されない。

        num_plot += 1

    return num_plot

def case4():

    fig, ax = plt.subplots()
    line, = ax.plot(np.random.randn(100))
    fig.canvas.draw()
    fig.show()

    t_start = time.time()
    num_plot = 0

    while time.time() - t_start < 1:
        line.set_ydata(np.random.randn(100))

        ax.draw_artist(ax.patch)
        ax.draw_artist(line)
        #fig.canvas.update()
        fig.canvas.blit(ax.bbox)

        fig.canvas.flush_events()
        num_plot += 1

    return num_plot

def case5():

    fig, ax = plt.subplots()
    fig.canvas.draw()

    bg = fig.canvas.copy_from_bbox(ax.bbox)

    line, = ax.plot(np.random.randn(100))
    fig.show()

    t_start = time.time()
    num_plot = 0

    while time.time() - t_start < 1:
        line.set_ydata(np.random.randn(100))

        fig.canvas.restore_region(bg)
        ax.draw_artist(line)

        #fig.canvas.update()
        fig.canvas.blit(ax.bbox)

        fig.canvas.flush_events()
        num_plot += 1

    return num_plot


def case6():

    fig, ax = plt.subplots()
    fig.canvas.draw()

    bg = fig.canvas.copy_from_bbox(ax.bbox)

    line, = ax.plot(np.random.randn(100))
    fig.show()

    t_start = time.time()
    num_plot = 0

    while time.time() - t_start < 1:
        line.set_ydata(np.random.randn(100))

        fig.canvas.restore_region(bg)
        ax.draw_artist(line)

        fig.canvas.update()

        fig.canvas.flush_events()
        num_plot += 1

    return num_plot


if __name__ == "__main__":
    print("case1: " + str(case1()) + "fps")
    print("case1: " + str(case2()) + "fps")
    print("case3: " + str(case3()) + "fps")
    print("case4: " + str(case4()) + "fps")
    print("case5: " + str(case5()) + "fps")
    print("case6: " + str(case6()) + "fps")