import numpy as np

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