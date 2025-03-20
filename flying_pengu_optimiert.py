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
GRAVITY = 9.81 * 0.5
JUMP_IMPULSE = GRAVITY * 0.2
KEY_ESC = 27
KEY_ENTER = 10
KEY_SPACE = 32

# Global variables
start_game = True
difficulty = 1


def display_screen(stdscr, screen_array):
    """Display a screen on the terminal."""
    # Only update what's changed (more efficient than clearing)
    for row in range(len(screen_array)):
        # Using addstr for entire row instead of individual characters
        stdscr.addstr(row, 0, ''.join(screen_array[row]))
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
            'wall_distance': 40 + wall_width,
            'gravity_per_frame': GRAVITY / 30  # Pre-calculate for efficiency
        }
    elif level == 2:
        return {
            'fps': 40,
            'opening_height': 10,
            'wall_distance': 40 + wall_width,
            'gravity_per_frame': GRAVITY / 40
        }
    else:  # level 3
        return {
            'fps': 50,
            'opening_height': 10,
            'wall_distance': 30 + wall_width,
            'gravity_per_frame': GRAVITY / 50
        }


def initialize_screen():
    """Create and return the initial game screen with borders."""
    # Using lists instead of numpy arrays for faster individual element updates
    screen = [[' ' for _ in range(TOTAL_WIDTH)] for _ in range(TOTAL_HEIGHT)]
    
    # Draw borders
    for i in range(TOTAL_WIDTH):
        screen[0][i] = '#'
        screen[TOTAL_HEIGHT-1][i] = '#'
    
    for i in range(TOTAL_HEIGHT):
        screen[i][0] = '#'
        screen[i][TOTAL_WIDTH-1] = '#'
    
    return screen


def update_penguin_physics(y, y_velocity, key, gravity_per_frame):
    """Update penguin position and velocity based on physics."""
    # Apply input
    if key == KEY_SPACE:
        y_velocity = -JUMP_IMPULSE
    else:
        y_velocity += gravity_per_frame
    
    # Update position
    y += y_velocity
    
    # Handle boundaries
    if y < 0:
        y = 0
        y_velocity = 0
    elif y > TOTAL_HEIGHT - PENGUIN_HEIGHT - 1:
        y = TOTAL_HEIGHT - PENGUIN_HEIGHT - 1
        y_velocity = 0
        
    return y, y_velocity


def shift_screen_left(screen):
    """Shift screen contents left efficiently."""
    for row in range(1, TOTAL_HEIGHT-1):
        for col in range(1, TOTAL_WIDTH-2):
            screen[row][col] = screen[row][col+1]
        screen[row][TOTAL_WIDTH-2] = ' '
    return screen


def check_collision_optimized(screen, penguin_art, y_start, x_start, penguin_mask):
    """Optimized collision detection."""
    for y_offset in range(PENGUIN_HEIGHT):
        for x_offset in range(PENGUIN_WIDTH):
            if penguin_mask[y_offset][x_offset]:
                y, x = y_start + y_offset, x_start + x_offset
                if screen[y][x] != ' ':
                    return True
    return False


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input

    global start_game, difficulty

    # Handle start screen
    if start_game:
        start_game = False
        if not handle_difficulty_selection(stdscr):
            return
    
    # Setup game parameters based on difficulty
    params = setup_difficulty_parameters(difficulty)
    fps = params['fps']
    opening_height = params['opening_height']
    wall_distance = params['wall_distance']
    wall_width = 8
    gravity_per_frame = params['gravity_per_frame']
    
    # Initialize game elements
    screen_array = initialize_screen()
    penguin = Penguin()
    penguin_art = penguin.fly()
    # Pre-compute penguin mask once
    penguin_mask = [[penguin_art[y][x] != ' ' for x in range(PENGUIN_WIDTH)] for y in range(PENGUIN_HEIGHT)]
    
    # Game state variables
    timesteps = 0
    offset = 6
    last_center = TOTAL_HEIGHT // 2
    start_draw_wall = False
    draw_wall_width = 0
    score = 0
    mast_count = 0
    y = 7.0  # Penguin's vertical position (float for smoother physics)
    y_velocity = 0.0
    frame_time = 1.0 / fps  # Pre-calculate frame time
    
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
                    start_game = True
                    difficulty = 1
                    return curses.wrapper(main)
                elif key == KEY_ENTER:
                    break
        
        # Shift screen contents left (optimized)
        screen_array = shift_screen_left(screen_array)

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
                    screen_array[i][TOTAL_WIDTH-2] = wall_piece[i-1]
            else:
                draw_wall_width = 0
                start_draw_wall = False

        # Update penguin physics (simplified calculation)
        y, y_velocity = update_penguin_physics(y, y_velocity, key, gravity_per_frame)
        
        # Update penguin position
        y_start = int(round(y))
        x_start = PENGUIN_X_START
        x_end = x_start + PENGUIN_WIDTH

        # Check for collision (optimized)
        collided = check_collision_optimized(screen_array, penguin_art, y_start, x_start, penguin_mask)

        # Update score (optimized check)
        found_mast = False
        for row in range(TOTAL_HEIGHT):
            if screen_array[row][x_end] == '_':
                found_mast = True
                break
                
        if found_mast:
            mast_count += 1
        else:
            mast_count = 0
            
        if mast_count == 2:
            score += 1
            mast_count = 0

        # Create screen copy only once after all modifications
        screen_with_penguin = [row[:] for row in screen_array]
        
        # Add penguin to display copy
        for y_offset in range(PENGUIN_HEIGHT):
            for x_offset in range(PENGUIN_WIDTH):
                if penguin_mask[y_offset][x_offset]:
                    py, px = y_start + y_offset, x_start + x_offset
                    if 0 <= py < TOTAL_HEIGHT and 0 <= px < TOTAL_WIDTH:
                        screen_with_penguin[py][px] = penguin_art[y_offset][x_offset]

        # Display score
        score_array = get_score_array(score)
        for i, char in enumerate(score_array):
            if i + 2 < TOTAL_WIDTH:
                screen_with_penguin[1][i+2] = char

        # Render the game screen
        display_screen(stdscr, screen_with_penguin)

        # Handle collision
        if collided:
            crash_screen = create_crash_screen(TOTAL_HEIGHT, TOTAL_WIDTH, score)
            display_screen(stdscr, crash_screen)
            
            while True:
                key = stdscr.getch()
                if key == KEY_ESC:
                    start_game = True
                    difficulty = 1
                    return curses.wrapper(main)
                elif key == KEY_ENTER:
                    return curses.wrapper(main)

        # Maintain frame rate more precisely
        elapsed_time = time.time() - start_time
        timesteps += 1
        sleep_time = frame_time - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)


if __name__ == "__main__":
    curses.wrapper(main)