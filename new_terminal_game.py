import time
import curses
import random
import numpy as np
from draw_penguin import draw_penguin

class Wall:
    def __init__(self, height, width, opening_height):
        self.height = height
        self.width = width
        self.opening_height = opening_height
        # Adjust opening_position relative to wall height
        self.opening_position = random.randint(opening_height//2, height - opening_height//2 - 1)

    def __str__(self):
        # Build list of rows using '#' except in the opening.
        rows = []
        for i in range(self.height):
            if i < self.opening_position - self.opening_height//2 or i >= self.opening_position + self.opening_height//2:
                rows.append("#" * self.width)
            else:
                rows.append(" " * self.width)
        return "\n".join(rows)

def main(stdscr):
    curses.curs_set(0)
    total_height, total_width = 20, 50

    # Create a 2D NumPy array for the screen filled with spaces.
    screen_array = np.full((total_height, total_width), ' ', dtype=str)

    # Create penquin array
    pengu_array = draw_penguin()

    # Draw initial border.
    screen_array[0, :] = '#'
    screen_array[total_height-1, :] = '#'
    screen_array[:, 0] = '#'
    screen_array[:, total_width-1] = '#'

    timesteps = 0
    wall_distance = 20
    opening_height = 7

    while True:
        # Shift the interior (non-border) left by one column.
        # Columns 1 to total_width-2 are the interior.
        screen_array[1:total_height-1, 1:total_width-2] = screen_array[1:total_height-1, 2:total_width-1]
        # Clear the new rightmost interior column.
        screen_array[1:total_height-1, total_width-2] = ' '

        # Every wall_distance steps, add a new wall in the new rightmost interior column.
        if timesteps % wall_distance == 0:
            # Create the wall for the interior only.
            wall = Wall(total_height-2, 1, opening_height)
            wall_lines = str(wall).split("\n")
            for i in range(1, total_height-1):
                screen_array[i, total_width-2] = wall_lines[i-1]

        screen_array[7:13, 15:26] = pengu_array

        # Reapply border (overwrite any changes in the border area).
        screen_array[0, :] = '#'
        screen_array[total_height-1, :] = '#'
        screen_array[:, 0] = '#'
        screen_array[:, total_width-1] = '#'

        # Render the array.
        stdscr.clear()
        for row in range(total_height):
            for col in range(total_width):
                stdscr.addch(row, col, screen_array[row, col])
        stdscr.refresh()

        time.sleep(0.01)
        timesteps += 1

if __name__ == "__main__":
    curses.wrapper(main)