import time
import curses
import random
import numpy as np


def main(stdscr):
    curses.curs_set(0)
    height, width = 20, 50

    # Create a 2D NumPy array for the screen
    screen_array = np.full((height, width), ' ', dtype=str)

    while True:
        # Clear array
        screen_array[:] = ' '

        # Draw border
        screen_array[0, :] = '#'
        screen_array[height-1, :] = '#'
        screen_array[:, 0] = '#'
        screen_array[:, width-1] = '#'

        # Place random points
        for _ in range(10):
            r = random.randint(1, height - 2)
            c = random.randint(1, width - 2)
            screen_array[r, c] = '*'

        # Render the array
        stdscr.clear()
        for row in range(height):
            for col in range(width):
                stdscr.addch(row, col, screen_array[row, col])
        stdscr.refresh()
        time.sleep(1)  # Aktualisiere alle 1 Sekunde

if __name__ == "__main__":
    curses.wrapper(main)