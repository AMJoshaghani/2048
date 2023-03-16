"""
    2048 in terminal!
    just run the file and have fun :)

by Amir M. Joshaghani - amjoshaghani.ir
"""
import curses
import time
import random
import numpy as np
from curses import wrapper

welcome_text = """
        ▒█░░▒█ ▒█▀▀▀ ▒█░░░ ▒█▀▀█ ▒█▀▀▀█ ▒█▀▄▀█ ▒█▀▀▀ 　 ▀▀█▀▀ ▒█▀▀▀█ 　 █▀█ █▀▀█ ░█▀█░ ▄▀▀▄ █      
        ▒█▒█▒█ ▒█▀▀▀ ▒█░░░ ▒█░░░ ▒█░░▒█ ▒█▒█▒█ ▒█▀▀▀ 　 ░▒█░░ ▒█░░▒█ 　 ░▄▀ █▄▀█ █▄▄█▄ ▄▀▀▄ ▀     
        ▒█▄▀▄█ ▒█▄▄▄ ▒█▄▄█ ▒█▄▄█ ▒█▄▄▄█ ▒█░░▒█ ▒█▄▄▄ 　 ░▒█░░ ▒█▄▄▄█ 　 █▄▄ █▄▄█ ░░░█░ ▀▄▄▀ ▄     
"""
blocks = np.zeros((4, 4), int)
is_started = False


def main(stdscr):
    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_MAGENTA)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)

    base_win = curses.newwin(100, 100, 9, 5)
    menu_pad = curses.newpad(100, 100)

    stdscr.refresh()
    base_win.refresh()
    stdscr.addstr(5, 37, " W E L C O M E   T O   2 0 4 8 ! ", curses.color_pair(2) | curses.A_REVERSE)

    for i in range(25):  # vertical border
        base_win.addstr(i, 23, '█' * 2)
        base_win.addstr(i, 75, '█' * 2)
    for i in range(50):  # horizontal border
        base_win.addstr(0, 25 + i, '█')
        base_win.addstr(24, 25 + i, '█')
    menu_pad.addstr(10, 10, welcome_text, curses.A_BOLD | curses.color_pair(1))
    base_win.addstr(17, 33, "Press any key to start. q for exit", curses.A_BLINK | curses.A_REVERSE)

    for i in range(1, 51):
        base_win.refresh()
        menu_pad.refresh(5, i, 10, 33, 20, 75)
        time.sleep(0.6 / i)

    def get_blocks():
        global blocks
        for row in blocks:
            for col in row:
                yield str(col)

    def show_blocks():
        insert_random()
        for r in range(1, 4):
            for o in range(0, 4):
                base_win.addstr(r * (6 + o // 4 * 6), 25 + 13 * o % 4, '░' * 47)
        for t in range(0, 3):
            for o in range(0, 23):
                base_win.addstr(o + t // 4 * 6 + 1, 35 + 13 * (t % 4), '░' * 2)

        for n, t in enumerate(get_blocks()):
            base_win.addstr(3 + (n // 4) * 6, 27 + 13 * (n % 4),
                            f"[{t.zfill(4)}]" if t != str(0) else "[    ]",
                            curses.color_pair(2) if t != str(0) else curses.color_pair(3) | curses.A_BOLD
                            )
        base_win.refresh()

    def insert_random():
        global blocks
        p, j = (blocks == 0).nonzero()
        if p.size != 0:
            rnd = random.randint(0, p.size - 1)
            blocks[p[rnd], j[rnd]] = 2 * ((random.random() > .9) + 1)

    def make_move(col):
        new_col = np.zeros(4, dtype=col.dtype)
        j = 0
        previous = None
        for e in range(col.size):
            if col[e] != 0:
                if previous is None:
                    previous = col[e]
                else:
                    if previous == col[e]:
                        new_col[j] = 2 * col[e]
                        j += 1
                        previous = None
                    else:
                        new_col[j] = previous
                        j += 1
                        previous = col[e]
        if previous is not None:
            new_col[j] = previous
        return new_col

    def move(direct):
        rotated_board = np.rot90(blocks, direct)
        cols = [rotated_board[f, :] for f in range(4)]
        new_board = np.array([make_move(col) for col in cols])
        return np.rot90(new_board, -direct)

    def shift(direction):
        global blocks
        prev_blocks = blocks[:]
        if direction == "KEY_UP":
            blocks = move(1)
            show_blocks()
        elif direction == "KEY_DOWN":
            blocks = move(3)
            show_blocks()
        elif direction == "KEY_LEFT":
            blocks = move(0)
            show_blocks()
        elif direction == "KEY_RIGHT":
            blocks = move(2)
            show_blocks()
        if (blocks == prev_blocks).all():
            base_win.addstr(27, 35, " "*50)
            base_win.addstr(27, 45, "Game Over!", curses.A_BLINK | curses.color_pair(4))

    while True:
        k = stdscr.getkey()
        if k != "q":
            global is_started
            if not is_started:
                global blocks
                base_win.addstr(27, 35, "Use arrow keys to move blocks!", curses.A_ITALIC)
                base_win.addstr(17, 33, " " * 40, curses.A_BLINK)
                menu_pad.clear()
                menu_pad.refresh(5, 0, 10, 32, 20, 75)
                show_blocks()
                is_started = True
            else:
                if k in ["KEY_LEFT", "KEY_RIGHT", "KEY_UP", "KEY_DOWN"]:
                    shift(k)
        else:
            break

    stdscr.clear()
    curses.echo()


if __name__ == "__main__":
    wrapper(main)
