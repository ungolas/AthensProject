import numpy as np

def draw_penguin():
    height, width = 20, 50
    pengu = np.full((height, width), ' ', dtype=str)

    # pengu_art = np.string_.array([
    #     "   .--.",
    #     "  |o_o |",
    #     "  |:_/ |",
    #     " //   \\ \\",
    #     "(:     :)",
    #     "  \\._./",
    #     "   _|_"
    # ])
    
    pengu_art = ["      __   ",
                 "    .' o)=-",
                 "   /.-.'   ",
                 "  //  |\   ",
                 "  ||  |'   ",
                 "_,:(_/_    "]
    
    pengu_array = np.array([list(line) for line in pengu_art])
    

    # for r, line in enumerate(pengu_art):
    #     for c, char in enumerate(line):
    #         screen_array[row + r, col + c] = char
    print(pengu_art)
    print(pengu_array)
    print(pengu_array.shape)
    return pengu_array

def main():
    screen_array = np.full((20, 50), ' ', dtype=str)
    draw_penguin(screen_array, 10, 25)

if __name__ == "__main__":
    main()