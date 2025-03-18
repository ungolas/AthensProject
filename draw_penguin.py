import numpy as np

def draw_penguin(screen_array, row, col):
    height, width = 20, 50
    pengu = np.full((height, width), ' ', dtype=str)

    pengu_art = np.string_.array([
        "   .--.",
        "  |o_o |",
        "  |:_/ |",
        " //   \\ \\",
        "(:     :)",
        "  \\._./",
        "   _|_"
    ])

    # for r, line in enumerate(pengu_art):
    #     for c, char in enumerate(line):
    #         screen_array[row + r, col + c] = char
    print(pengu_art)

def main():
    
    draw_penguin()

if __name__ == "__main__":
    main()