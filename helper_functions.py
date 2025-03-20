import numpy as np
import math

# debug function to print to file
def print2file(output_string):
    with open('output.txt', 'a') as f:
        print(output_string, file=f)


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
    pause_screen[center_height - 3, center_width - math.floor(len(str_paused)/2):center_width + math.ceil(len(str_paused)/2)] = list(str_paused)
    pause_screen[center_height, center_width - math.floor(len(str_press)/2):center_width + math.ceil(len(str_press)/2)] = list(str_press)
    pause_screen[center_height + 2, center_width - math.floor(len(str_score)/2):center_width + math.ceil(len(str_score)/2)] = list(str_score)
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
    pause_screen[center_height - 3, center_width - math.floor(len(str_paused)/2):center_width + math.ceil(len(str_paused)/2)] = list(str_paused)
    pause_screen[center_height, center_width - math.floor(len(str_press)/2):center_width + math.ceil(len(str_press)/2)] = list(str_press)
    pause_screen[center_height + 2, center_width - math.floor(len(str_score)/2):center_width + math.ceil(len(str_score)/2)] = list(str_score)
    return pause_screen