import time
import curses
import random

def main(stdscr):
    curses.curs_set(0)  # Versteckt den Cursor
    height, width = 20, 50  # Hintergrundgröße

    while True:
        stdscr.clear()
        # Beispiel: Einfacher Rahmen fürs "Hintergrundfenster"
        for row in range(height):
            for col in range(width):
                if row in (0, height-1) or col in (0, width-1):
                    stdscr.addch(row, col, '#')
                else:
                    stdscr.addch(row, col, ' ')
        
        # Zeichne zufällige Punkte
        for _ in range(10):
            rand_row = random.randint(1, height - 2)
            rand_col = random.randint(1, width - 2)
            stdscr.addch(rand_row, rand_col, '*')

        stdscr.refresh()
        time.sleep(1)  # Aktualisiere alle 1 Sekunde

if __name__ == "__main__":
    curses.wrapper(main)