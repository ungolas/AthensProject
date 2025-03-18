import time
import curses
import math
import random
import numpy as np
from draw_penguin import draw_penguin_wings_down, draw_penguin_wings_up

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
    
class Penguin:
    def __init__(self):
        self.height = 6
        self.width = 12
        self.ascii_art = self.wings_up()
        self.fly_status = True
        self.timesteps = 0

    def fly(self):
        self.timesteps += 1
        if self.timesteps % 10 == 0:
            self.fly_status = not self.fly_status
            self.timesteps = 0
            if(self.fly_status):
                self.ascii_art = self.wings_down()
            else:
                self.ascii_art = self.wings_up()
        return self.ascii_art
    
    def wings_down(self):
        pengu_art = ["       __   ",
                     "     .' o)=-",
                     "    /.-.'   ",
                     "   //  |\   ",
                     "   ||  |'   ",
                     " _,:(_/_    "]
        pengu_array = np.array([list(line) for line in pengu_art])
        return pengu_array
    
    def wings_up(self):
        pengu_art = ["       __   ",
                     "     .' o)=-",
                     " _  /.-.',_ ",
                     "  \,/  |/   ",
                     "   ||  |'   ",
                     " _,:(_/_    "]
        pengu_array = np.array([list(line) for line in pengu_art])
        return pengu_array


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)  # This allows getch() to be non-blocking

    total_height, total_width = 20, 50

    # Create a 2D NumPy array for the screen filled with spaces.
    screen_array = np.full((total_height, total_width), ' ', dtype=str)

    # Create penquin array
    penguin = Penguin()

    # Draw initial border.
    screen_array[0, :] = '#'
    screen_array[total_height-1, :] = '#'
    screen_array[:, 0] = '#'
    screen_array[:, total_width-1] = '#'

    timesteps = 0
    wall_distance = 20
    opening_height = 7

    # Current score
    score = 0

    # Pause flag
    paused = False

    while True:
        # Track the pressed keys
        key = stdscr.getch()

        if key == 27:
            paused = True
            pause_screen = create_pause_screen(total_height, total_width, score)
            stdscr.clear()
            for row in range(total_height):
                for col in range(total_width):
                    stdscr.addch(row, col, pause_screen[row, col])
            stdscr.refresh()
            while paused:
                key = stdscr.getch()
                if key == 27:
                    curses.endwin()  # Bildschirm zurücksetzen
                    return           # main() verlassen -> zurück ins Terminal
                elif key == 10:
                    paused = False

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

        screen_array[7:13, 14:26] = penguin.fly()

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

def create_pause_screen(height, width, score):
    center_width = width // 2
    center_height = height // 2
    pause_screen = np.full((height, width), ' ', dtype=str)

    str_paused = "GAME PAUSED"
    str_press = "Press Enter to resume or ESC to quit"
    str_score = f"Score: {score}"
    pause_screen[center_height - 1, center_width - math.floor(len(str_paused)/2):center_width + math.ceil(len(str_paused)/2)] = list(str_paused)
    pause_screen[center_height, center_width - math.floor(len(str_press)/2):center_width + math.ceil(len(str_press)/2)] = list(str_press)
    pause_screen[center_height + 1, center_width - math.floor(len(str_score)/2):center_width + math.ceil(len(str_score)/2)] = list(str_score)
    return pause_screen

if __name__ == "__main__":
    curses.wrapper(main)