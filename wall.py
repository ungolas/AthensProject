import random
import math

class Wall:
    def __init__(self, height, width, opening_height, offset, last_center):
        self.height = height
        self.width = width
        self.opening_height = opening_height
        # Adjust opening_position relative to wall height
        upper_bound = min(last_center + offset, height - math.ceil(opening_height/2)-1)
        lower_bound = max(last_center - offset, math.ceil(opening_height/2)+1)
        self.opening_position = random.randint(lower_bound, upper_bound)