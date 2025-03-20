import time
import curses
import math
import random
import numpy as np
from wall import Wall
from penguin import Penguin
from helper_functions import *

# Constants
TOTAL_HEIGHT = 30
TOTAL_WIDTH = 150
PENGUIN_HEIGHT = 6
PENGUIN_WIDTH = 12
PENGUIN_X_START = 14
GRAVITY = 5 * 9.81
JUMP_IMPULSE = 20
KEY_ESC = 27
KEY_ENTER = 10
KEY_SPACE = 32

# Global variables
start_game = True
difficulty = 1


def display_screen(stdscr, screen_array):
    """Display a screen on the terminal."""
    stdscr.clear()
    for row in range(len(screen_array)):
        for col in range(len(screen_array[0])):
            stdscr.addch(row, col, screen_array[row, col])
    stdscr.refresh()


def handle_difficulty_selection(stdscr):
    """Show start screen and get user difficulty selection."""
    global start_game, difficulty
    
    start_screen = create_start_screen(TOTAL_HEIGHT, TOTAL_WIDTH)
    display_screen(stdscr, start_screen)
    
    while True:
        key = stdscr.getch()
        if key == 49:  # 1 key
            difficulty = 1
            break
        elif key == 50:  # 2 key
            difficulty = 2
            break
        elif key == 51:  # 3 key
            difficulty = 3
            break
        elif key == KEY_ESC:
            return False
    
    return True


def setup_difficulty_parameters(level):
    """Set game parameters based on difficulty level."""
    wall_width = 8
    
    if level == 1:
        return {
            'fps': 30,
            'opening_height': 12,
            'wall_distance': 40 + wall_width
        }
    elif level == 2:
        return {
            'fps': 40,
            'opening_height': 10,
            'wall_distance': 40 + wall_width
        }
    else:  # level 3
        return {
            'fps': 50,
            'opening_height': 10,
            'wall_distance': 30 + wall_width
        }


def initialize_screen():
    """Create and return the initial game screen with borders."""
    screen = np.full((TOTAL_HEIGHT, TOTAL_WIDTH), ' ', dtype=str)
    # Draw borders
    screen[0, :] = '#'
    screen[TOTAL_HEIGHT-1, :] = '#'
    screen[:, 0] = '#'
    screen[:, TOTAL_WIDTH-1] = '#'
    return screen


def update_penguin_physics(y, y_velocity, key, fps):
    """Update penguin position and velocity based on physics."""
    # Apply input
    if key == KEY_SPACE:
        y_velocity = -JUMP_IMPULSE
    else:
        y_velocity += GRAVITY * (1/fps)
    
    # Update position
    y += y_velocity * (1/fps)
    
    # Handle boundaries
    if y < 0:
        y = 0
        y_velocity = 0
    elif y > TOTAL_HEIGHT - PENGUIN_HEIGHT - 1:
        y = TOTAL_HEIGHT - PENGUIN_HEIGHT - 1
        y_velocity = 0
        
    return y, y_velocity


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input

    global start_game, difficulty

    # Handle start screen
    if start_game:
        start_game = False
        if not handle_difficulty_selection(stdscr):
            curses.endwin()
            return
    
    # Setup game parameters based on difficulty
    params = setup_difficulty_parameters(difficulty)
    fps = params['fps']
    opening_height = params['opening_height']
    wall_distance = params['wall_distance']
    wall_width = 8
    
    # Initialize game elements
    screen_array = initialize_screen()
    penguin = Penguin()
    penguin_mask = penguin._wings_up_art != ' '
    
    # Game state variables
    timesteps = 0
    offset = 6
    last_center = TOTAL_HEIGHT // 2
    start_draw_wall = False
    draw_wall_width = 0
    current_wall = None
    score = 0
    mast_count = 0
    y = 7  # Penguin's vertical position
    y_velocity = 0
    
    # Main game loop
    while True:
        # Track frame time
        start_time = time.time()
        
        # Get user input
        key = stdscr.getch()

        # Handle pause screen
        if key == KEY_ESC:
            pause_screen = create_pause_screen(TOTAL_HEIGHT, TOTAL_WIDTH, score)
            display_screen(stdscr, pause_screen)
            
            while True:
                key = stdscr.getch()
                if key == KEY_ESC:
                    curses.endwin()
                    start_game = True
                    difficulty = 1
                    return curses.wrapper(main)
                elif key == KEY_ENTER:
                    break
        
        # Shift screen contents left
        screen_array[1:TOTAL_HEIGHT-1, 1:TOTAL_WIDTH-2] = screen_array[1:TOTAL_HEIGHT-1, 2:TOTAL_WIDTH-1]
        screen_array[1:TOTAL_HEIGHT-1, TOTAL_WIDTH-2] = ' '

        # Create new wall when needed
        if timesteps % wall_distance == 0:
            start_draw_wall = True
            current_wall = Wall(TOTAL_HEIGHT-2, wall_width, opening_height, offset, last_center)
            last_center = current_wall.opening_position
            
        # Draw wall pieces
        if start_draw_wall:
            draw_wall_width += 1
            if draw_wall_width <= wall_width:
                wall_piece = draw_wall(TOTAL_HEIGHT, wall_width, opening_height, last_center, draw_wall_width)
                for i in range(1, TOTAL_HEIGHT-1):
                    screen_array[i, TOTAL_WIDTH-2] = wall_piece[i-1]
            else:
                draw_wall_width = 0
                start_draw_wall = False

        # Update penguin physics
        y, y_velocity = update_penguin_physics(y, y_velocity, key, fps)
        
        # Update penguin position
        y_start = round(y)
        y_end = y_start + PENGUIN_HEIGHT
        x_start = PENGUIN_X_START
        x_end = x_start + PENGUIN_WIDTH

        # Add penguin to screen
        screen_with_penguin = screen_array.copy()
        screen_with_penguin[y_start:y_end, x_start:x_end][penguin_mask] = penguin.fly()[penguin_mask]

        # Check for collision
        collided = check_collision(
            screen_array[y_start:y_end, x_start:x_end], 
            screen_with_penguin[y_start:y_end, x_start:x_end]
        )

        # Update score
        if '_' in screen_array[:, x_end]:
            mast_count += 1
        else:
            mast_count = 0
            
        if mast_count == 2:
            score += 1

        # Display score
        score_array = get_score_array(score)
        screen_with_penguin[1, 2:2+len(score_array)] = score_array

        # Restore borders
        screen_with_penguin[0, :] = '#'
        screen_with_penguin[TOTAL_HEIGHT-1, :] = '#'
        screen_with_penguin[:, 0] = '#'
        screen_with_penguin[:, TOTAL_WIDTH-1] = '#'

        # Render the game screen
        display_screen(stdscr, screen_with_penguin)

        # Handle collision
        if collided:
            crash_screen = create_crash_screen(TOTAL_HEIGHT, TOTAL_WIDTH, score)
            display_screen(stdscr, crash_screen)
            
            while True:
                key = stdscr.getch()
                if key == KEY_ESC:
                    curses.endwin()
                    start_game = True
                    difficulty = 1
                    return curses.wrapper(main)
                elif key == KEY_ENTER:
                    curses.endwin()
                    return curses.wrapper(main)

        # Maintain frame rate
        elapsed_time = time.time() - start_time
        timesteps += 1
        if elapsed_time < 1/fps:
            time.sleep((1/fps) - elapsed_time)


if __name__ == "__main__":
    curses.wrapper(main)