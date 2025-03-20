import time
import curses
import math
import random
import numpy as np

# Global variable to start the game and choose the difficulty
start_game = True
difficulty = 1

# help function
def print2file(output_string):
    with open('output.txt', 'a') as f:
        print(output_string, file=f)

class Wall:
    def __init__(self, height, width, opening_height, offset, last_center):
        self.height = height
        self.width = width
        self.opening_height = opening_height
        # Adjust opening_position relative to wall height
        upper_bound = min(last_center + offset, height - math.ceil(opening_height/2)-1)
        lower_bound = max(last_center - offset, math.ceil(opening_height/2)+1)
        self.opening_position = random.randint(lower_bound, upper_bound)

    
class Penguin:
    def __init__(self):
        self.height = 6
        self.width = 12
        # Pre-calculate both art states once
        self._wings_up_art = self.wings_up()
        self._wings_down_art = self.wings_down()
        self.ascii_art = self._wings_up_art
        self.fly_status = False
        self.timesteps = 0

    def fly(self):
        self.timesteps += 1
        if self.timesteps % 10 == 0:
            self.fly_status = not self.fly_status
            self.timesteps = 0
            self.ascii_art = self._wings_down_art if self.fly_status else self._wings_up_art
        return self.ascii_art
    
    def wings_down(self):
        pengu_art = ["       __   ",
                     "     .' o)=-",
                     "    /.-.'   ",
                     "  _//  |\_  ",
                     "   ||  |'   ",
                     " _,:(_/_    "]
        return np.array([list(line) for line in pengu_art])
    
    def wings_up(self):
        pengu_art = ["       __   ",
                     "     .' o)=-",
                     " _  /.-.' _ ",
                     "  \,/  |,/  ",
                     "   ||  |'   ",
                     " _,:(_/_    "]
        return np.array([list(line) for line in pengu_art])


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)  # This allows getch() to be non-blocking

    global start_game, difficulty

    total_height, total_width = 30, 150

    # Create a 2D NumPy array for the screen filled with spaces.
    screen_array = np.full((total_height, total_width), ' ', dtype=str)

    # Create penquin array
    penguin = Penguin()

    # Draw initial border.
    screen_array[0, :] = '#'
    screen_array[total_height-1, :] = '#'
    screen_array[:, 0] = '#'
    screen_array[:, total_width-1] = '#'

    # Variables for the walls
    timesteps = 0
    wallwidth = 8                   # width of the wall
    wall_distance = 40 + wallwidth  # horizontal distance between consecutive walls
    opening_height = 12            # height of the opening in the wall
    offset = 6                      # maximum vertical offset of the center points of consecutive walls
    last_center = total_height//2   # initial center point of the opening
    start_draw_wall = False
    draw_wall_width = 0
    current_wall = None

    # Current score
    score = 0

    # Pause flag
    paused = False

    # fps
    fps = 30

    # gravity
    g = 5*9.81

    # impulse
    imp = 20

    # Initialization of the starting position of the penguin
    y_start=7
    y_end=13
    x_start=14
    x_end=26

    # mastcount for score
    mastcount=0

    # setup height tracking
    # going to track the upper left corner of the penguin
    y = y_start
    y_p = 0

    if start_game:
        # Create the start screen and wait for the user to choose a difficulty.
        start_game = False
        start_screen = create_start_screen(total_height, total_width)
        stdscr.clear()
        for row in range(total_height):
            for col in range(total_width):
                stdscr.addch(row, col, start_screen[row, col])
        stdscr.refresh()
        while True:
            key = stdscr.getch()
            if key == 49:
                difficulty = 1
                break
            elif key == 50:
                difficulty = 2
                break
            elif key == 51:
                difficulty = 3
                break
            elif key == 27:
                curses.endwin()  # reset the terminal
                return           # exit main() function
            
    if difficulty == 1:
        fps = 30
        opening_height = 12
    elif difficulty == 2:
        fps = 40
        opening_height = 10
    elif difficulty == 3:
        fps = 50
        opening_height = 10
        wall_distance = 30 + wallwidth


    while True:

        # track time
        start_time = time.time()
        
        # Track the pressed keys
        key = stdscr.getch()

        # Check if the key is ESC -> Pause Screen
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
                    curses.endwin()  # reset the terminal
                    start_game = True
                    difficulty = 1
                    return curses.wrapper(main)          
                elif key == 10:
                    paused = False   # resume the game
        
        # Shift the interior (non-border) left by one column.
        # Columns 1 to total_width-2 are the interior.
        screen_array[1:total_height-1, 1:total_width-2] = screen_array[1:total_height-1, 2:total_width-1]
        # Clear the new rightmost interior column.
        screen_array[1:total_height-1, total_width-2] = ' '

        # Every wall_distance steps, add a new wall in the new rightmost interior column.
        if timesteps % wall_distance == 0:
            start_draw_wall = True
            current_wall = Wall(total_height-2, wallwidth, opening_height, offset, last_center)
            last_center = current_wall.opening_position
            
        if start_draw_wall:
            draw_wall_width += 1
            if draw_wall_width <= wallwidth:
                wall_piece = draw_wall(total_height, wallwidth, opening_height, last_center, draw_wall_width)
                for i in range(1, total_height-1):
                    screen_array[i, total_width-2] = wall_piece[i-1]
            else:
                draw_wall_width = 0
                start_draw_wall = False

        # if spacebar is active the penguin jumps
        if key == 32:
            y_p = - imp
        else:
            y_p = y_p + g * (1/fps)

        # update the position of the penguin
        y = y + (y_p * (1/fps))

        # check if the penguin is out of the screen
        if y < 0:
            y = 0
            y_p = 0
        elif y > total_height-7:
            y = total_height-7
            y_p = 0

        # update the position of the penguin
        # print2file(y)
        y_start = round(y)
        y_end = y_start+6

        # Update the screen array with the penguin's new position.
        screen_array_pengu = screen_array.copy()
        screen_array_pengu[y_start:y_end, x_start:x_end] = penguin.fly()

        # Check for collision between the penguin and the wall.
        collided = check_collision(screen_array[y_start:y_end, x_start:x_end], screen_array_pengu[y_start:y_end, x_start:x_end])

        # method for counting the score
        if '_' in screen_array[:, x_end]:
            mastcount+=1
        else:
            mastcount=0
        if mastcount==2:
            score+=1

        # Show score in the top left corner
        score_array = get_score_array(score)
        screen_array_pengu[1, 2:2+len(score_array)] = score_array

        # Reapply border (overwrite any changes in the border area).
        screen_array_pengu[0, :] = '#'
        screen_array_pengu[total_height-1, :] = '#'
        screen_array_pengu[:, 0] = '#'
        screen_array_pengu[:, total_width-1] = '#'

        # Render the array.
        stdscr.clear()
        for row in range(total_height):
            for col in range(total_width):
                stdscr.addch(row, col, screen_array_pengu[row, col])
        stdscr.refresh()

        # Check if the penguin collided with the wall.
        if(collided==True):
            paused = True
            pause_screen = create_crash_screen(total_height, total_width, score)
            stdscr.clear()
            for row in range(total_height):
                for col in range(total_width):
                    stdscr.addch(row, col, pause_screen[row, col])
            stdscr.refresh()
            while paused:
                key = stdscr.getch()
                if key == 27:
                    curses.endwin()  # reset the terminal
                    start_game = True
                    difficulty = 1
                    return curses.wrapper(main)          
                elif key == 10:
                    curses.endwin()  # reset the terminal
                    return curses.wrapper(main)

        # Calculate the time to sleep to maintain 30 frames per second.
        elapsed_time = time.time() - start_time
        timesteps += 1
        if elapsed_time < 1/fps:
            time.sleep((1/fps) - elapsed_time)

        # Debug 30fps runtime
        # print2file(time.time()-start_time)

def draw_wall(height, wallwidth, opening_height, opening_position, current_wall_piece):
    """ Creates a single vertical slice of a wall with an opening.
    Args:
        height (int): The total height of the wall.
        wallwidth (int): The width of the wall (number of slices).
        opening_height (int): The height of the opening in the wall.
        opening_position (int): The vertical center position of the opening.
        current_wall_piece (int): The current slice of the wall being drawn (1 to wallwidth).
    Returns:
        np.ndarray: A 1D array representing the vertical slice of the wall.
    """
    if current_wall_piece == 1 or current_wall_piece == wallwidth:
        wall_piece = np.full((height-2), '|', dtype=str)
        wall_piece[opening_position - math.ceil(opening_height/2):opening_position + math.ceil(opening_height/2)] = ' '
        return wall_piece
    elif current_wall_piece > 1 and current_wall_piece < wallwidth:
        wall_piece = np.full((height-2), ' ', dtype=str)
        wall_piece[opening_position + math.ceil(opening_height/2)-1] = '_'
        wall_piece[opening_position - math.ceil(opening_height/2)-1] = '_'
        return wall_piece
    else:
        return np.full((height), ' ', dtype=str)
    
def get_score_array(score):
    """ Creates a NumPy array representing the current score.
    Args:
        score (_type_): The current score of the player.
    Returns:
        _type_: A NumPy array representing the current score.
    """
    str_score = "Score: " + str(score)
    score_array = np.array(list(str_score))
    return score_array
        
def check_collision(screen_array, penguin_art):
    """ Checks for a collision between the penguin and the wall.
    Args:
        screen_array (np.ndarray): A 2D array representing the current screen state.
        penguin_art (np.ndarray): A 2D array representing the penguin's ASCII art.
    Returns:
        bool: True if a collision is detected, False otherwise.
    """
    # Only check wall characters ('|') against non-space penguin characters
    for r in range(penguin_art.shape[0]):
        for c in range(penguin_art.shape[1]):
            if screen_array[r, c] == '|' and penguin_art[r, c] != ' ':
                return True
    return False

def create_start_screen(height, width):
    """ Creates the start screen with options to choose the difficulty.
    Args:
        height (int): The height of the screen.
        width (int): The width of the screen.
    Returns:
        np.ndarray: A 2D array representing the pause screen.
    """
    center_width = width // 2
    center_height = height // 2
    start_screen = np.full((height, width), ' ', dtype=str)

    str_name = "Pengu Fly"
    str_press = "Chosse the difficulty by pressing the number:"
    str_easy = "1 - Easy"
    str_medium = "2 - Medium"
    str_hard = "3 - Hard"
    str_esc = "Press ESC to quit the game"
    start_screen[center_height - 5, center_width - math.floor(len(str_name)/2):center_width + math.ceil(len(str_name)/2)] = list(str_name)
    start_screen[center_height - 2, center_width - math.floor(len(str_press)/2):center_width + math.ceil(len(str_press)/2)] = list(str_press)
    start_screen[center_height, center_width - math.floor(len(str_easy)/2):center_width + math.ceil(len(str_easy)/2)] = list(str_easy)
    start_screen[center_height + 1, center_width - math.floor(len(str_medium)/2):center_width + math.ceil(len(str_medium)/2)] = list(str_medium)
    start_screen[center_height + 2, center_width - math.floor(len(str_hard)/2):center_width + math.ceil(len(str_hard)/2)] = list(str_hard)
    start_screen[center_height + 3, center_width - math.floor(len(str_esc)/2):center_width + math.ceil(len(str_esc)/2)] = list(str_esc)
    return start_screen


def create_pause_screen(height, width, score):
    """ Creates the pause screen with a message and the current score.
    Args:
        height (int): The height of the screen.
        width (int): The width of the screen.
        score (int): The current score of the player.
    Returns:
        np.ndarray: A 2D array representing the pause screen.
    """
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

def create_crash_screen(height, width, score):
    """ Creates the crash screen with a game over message and the final score.
    Args:
        height (int): The height of the screen.
        width (int): The width of the screen.
        score (int): The final score of the player.
    Returns:
        np.ndarray: A 2D array representing the crash screen.
    """
    center_width = width // 2
    center_height = height // 2
    pause_screen = np.full((height, width), ' ', dtype=str)

    str_paused = "GAME OVER"
    str_press = "Press Enter to start again or ESC to quit"
    str_score = f"Score: {score}"
    pause_screen[center_height - 1, center_width - math.floor(len(str_paused)/2):center_width + math.ceil(len(str_paused)/2)] = list(str_paused)
    pause_screen[center_height, center_width - math.floor(len(str_press)/2):center_width + math.ceil(len(str_press)/2)] = list(str_press)
    pause_screen[center_height + 1, center_width - math.floor(len(str_score)/2):center_width + math.ceil(len(str_score)/2)] = list(str_score)
    return pause_screen

if __name__ == "__main__":
    curses.wrapper(main)