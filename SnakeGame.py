import PySimpleGUI as sg
from time import time
from random import randint


def convert_pos(cell):
    tl = cell[0] * cell_SIZE, cell[1] * cell_SIZE
    br = tl[0] + cell_SIZE, tl[1] + cell_SIZE
    return tl, br


def place_aplle():
    apple_pos = (randint(0, cell_NUM - 1), randint(0, cell_NUM - 1))
    while apple_pos in snake_BODY:
        apple_pos = (randint(0, cell_NUM - 1), randint(0, cell_NUM - 1))
    return apple_pos


FIELD_SIZE = 400
cell_NUM = 10
cell_SIZE = FIELD_SIZE / cell_NUM

snake_BODY = [(4, 4), (3, 4), (2, 4)]
DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "up": (0, 1), "down": (0, -1)}
direction = DIRECTIONS["up"]
apple_pos = place_aplle()
apple_EAT = False

sg.theme("green")
field = sg.Graph(canvas_size=(FIELD_SIZE, FIELD_SIZE),
                 graph_bottom_left=(0, 0),
                 graph_top_right=(FIELD_SIZE, FIELD_SIZE),
                 background_color="black")
layout = [[field]]

window = sg.Window("SNAKE", layout, return_keyboard_events=True)

start_TIME = time()
while True:
    event, values = window.read(timeout=160)

    if event == sg.WIN_CLOSED: break

    if event == "Left:37": direction = DIRECTIONS["left"]
    if event == "Up:38": direction = DIRECTIONS["up"]
    if event == "Right:39": direction = DIRECTIONS["right"]
    if event == "Down:40": direction = DIRECTIONS["down"]

    time_sinceSTART = time() - start_TIME
    if start_TIME >= 0.5:
        start_TIME = time()

        if snake_BODY[0] == apple_pos:
            apple_pos = place_aplle()
            apple_EAT = True

        new_HEAD = (snake_BODY[0][0] + direction[0], snake_BODY[0][1] + direction[1])
        snake_BODY.insert(0, new_HEAD)
        if not apple_EAT:
            snake_BODY.pop()
        apple_EAT = False

        if not 0 <= snake_BODY[0][0] <= cell_NUM - 1 or \
                not 0 <= snake_BODY[0][0] <= cell_NUM - 1 or \
                snake_BODY[0] in snake_BODY[1:]:
            break

        field.DrawRectangle((0, 0), (FIELD_SIZE, FIELD_SIZE), "black")

        tl, br = convert_pos(apple_pos)
        field.DrawRectangle(tl, br, "red")

        for index, part in enumerate(snake_BODY):
            tl, br = convert_pos(part)
            color = "yellow" if index == 0 else "green"
            field.DrawRectangle(tl, br, color)

window.close()