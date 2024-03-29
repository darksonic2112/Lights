import pygame
import pandas as pd

pygame.init()
#  Enter "lights1" (1-5) or "lights-small-1" (1-5) for the different mazes
maze_name = "lights-small-1.csv"
maze_dir = ("lights-puzzles\\" + maze_name)

white = (255, 255, 255)
dark_grey = (25, 25, 25)
grey = (50, 50, 50)
yellow = (255, 255, 0)

menu_size = 120
block_size = 30

LEFT_MOUSEBUTTON = 1
RIGHT_MOUSEBUTTON = 3

turn_light_on = 100
turn_light_off = -100

#  Small size field: 14x14 blocks
#  Mid-size field: 25x25 blocks
#  block size is set by the variable "block_size" of the size block_size * block_size
#  block_size should be dividable by window_width and window_height, so that modulo equals 0
if maze_name[6] == "-":  # "-" for the distinction of "lights" and "lights-small" puzzles
    window_width = block_size * 14 + menu_size
    window_height = block_size * 14
else:
    window_width = block_size * 25 + menu_size
    window_height = block_size * 25

font = pygame.font.Font(None, 30)
reset_font = pygame.font.Font(None, 20)

rows, cols = (window_width // block_size, window_height // block_size)
maze_field = [[0 for i in range(cols)] for j in range(rows)]

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Lights")

light_bulb = pygame.image.load("assets\\lightbulb.png")

block_position_x = 0
block_position_y = 0

turn_counter = 0
turn_counter_text = font.render("Turn: " + str(turn_counter), False, white)

ran = False

reset_button_text = "Reset Game"
reset_button_rect = pygame.Rect(0, 0, 100, 50)

numbers = []
for index in range(5):
    numbers.append(index)


def get_block_at_mouse_position(mouse_x, mouse_y):
    column = mouse_x // block_size
    row = mouse_y // block_size
    return column, row


def update_counter():
    global turn_counter
    turn_counter += 1
    turn_counter_text = font.render("Turn: " + str(turn_counter), False, white)
    window.fill(dark_grey)
    window.blit(turn_counter_text, (window_width - 100, 10))


def update_block_position():
    global block_position_x, block_position_y
    block_position_x += 30
    if block_position_x >= window_width - menu_size:
        block_position_y += 30
        block_position_x = 0
    if block_position_y >= window_height:
        block_position_x = 0
        block_position_y = 0


def draw_field():
    global block_position_x, block_position_y, ran
    df = pd.read_csv(maze_dir, header=None, sep=";")
    for column_letter in range(len(df)):
        for row_letter in range(len(df[column_letter])):
            if df[row_letter][column_letter] == "x":
                draw_block(block_position_x, block_position_y, dark_grey)
            elif float(df[row_letter][column_letter]) in numbers:
                number = df[row_letter][column_letter]
                number = str(number)
                draw_block(block_position_x, block_position_y, dark_grey, number)
            else:
                draw_block(block_position_x, block_position_y, white)
            update_block_position()
        for column in range((window_width - menu_size) // block_size):
            for row in range(len(maze_field[column])):
                if isinstance(maze_field[row][column], int):
                    if maze_field[row][column] >= 100:
                        window.blit(light_bulb, (column * 30 + 3, row * 30 + 3))  # +3 to get it centered
                    elif maze_field[row][column] >= 1:
                        draw_lit_blocks(column * 30, row * 30)
    reset_button_surface = reset_font.render(reset_button_text, True, white)
    reset_text_rect = reset_button_surface.get_rect()
    reset_text_rect.center = reset_button_rect.center
    reset_button_rect.center = (window_width - menu_size + 60, 60)
    ran = True

    mouse = pygame.mouse.get_pos()

    if (window_width - menu_size + 10 <= mouse[0] <= window_width - menu_size + 10 + reset_button_rect.width and
            33 <= mouse[1] <= 33 + reset_button_rect.height): #  10 and 33 are offset numbers to align in the graphic
        pygame.draw.rect(window, (70, 70, 70), reset_button_rect)
    else:
        pygame.draw.rect(window, grey, reset_button_rect)

    window.blit(reset_button_surface, reset_text_rect)


def draw_block(block_position_x, block_position_y, color, number=None):
    column = block_position_x // block_size
    row = block_position_y // block_size
    rect = pygame.Rect(block_position_x, block_position_y, block_size, block_size)
    pygame.draw.rect(window, color, rect)
    pygame.draw.rect(window, dark_grey, rect, 2)
    if number:
        number_surface = font.render(str(int(float(number))), True, white)
        number_text_rect = number_surface.get_rect()
        number_text_rect.center = rect.center
        text_x = rect.centerx - number_text_rect.width / 2
        text_y = rect.centery - number_text_rect.height / 2
        window.blit(number_surface, (text_x, text_y))
        if not ran:
            maze_field[row][column] = ["number_block", int(float(number))]
    elif color == dark_grey:
        maze_field[row][column] = "empty_block"


def get_number_blocks(row, column, operator):
    if isinstance(maze_field[row - 1][column], list):
        maze_field[row - 1][column][1] += operator
    if isinstance(maze_field[row + 1][column], list):
        maze_field[row + 1][column][1] += operator
    if isinstance(maze_field[row][column - 1], list):
        maze_field[row][column - 1][1] += operator
    if column + 1 < (window_width - menu_size) // block_size:
        if isinstance(maze_field[row][column + 1], list):
            maze_field[row][column + 1][1] += operator


def update_light_source(light_bulb_position_x, light_bulb_position_y, state):
    column = light_bulb_position_x // block_size
    row = light_bulb_position_y // block_size
    if isinstance(maze_field[row][column], int):
        if state == turn_light_on and maze_field[row][column] == 0:
            get_lit_blocks(row, column, 1)
            get_number_blocks(row, column, -1)
            maze_field[row][column] += state
            update_counter()
        elif state == turn_light_off and maze_field[row][column] == turn_light_on:
            get_lit_blocks(row, column, -1)
            get_number_blocks(row, column, 1)
            maze_field[row][column] += state
            update_counter()


def get_lit_blocks(row, column, operator):
    current_row = row + 1
    while current_row in range((window_width - menu_size) // block_size):
        if isinstance(maze_field[current_row][column], int):
            if maze_field[current_row][column] >= 0:
                maze_field[current_row][column] += operator
                current_row += 1
        else:
            break
    current_row = row - 1
    while current_row in range((window_width - menu_size) // block_size):
        if isinstance(maze_field[current_row][column], int):
            if maze_field[current_row][column] >= 0:
                maze_field[current_row][column] += operator
                current_row -= 1
        else:
            break
    current_column = column + 1
    while current_column in range(window_height // block_size):
        if isinstance(maze_field[row][current_column], int):
            if maze_field[row][current_column] >= 0:
                maze_field[row][current_column] += operator
                current_column += 1
        else:
            break
    current_column = column - 1
    while current_column in range(window_height // block_size):
        if isinstance(maze_field[row][current_column], int):
            if maze_field[row][current_column] >= 0:
                maze_field[row][current_column] += operator
                current_column -= 1
        else:
            break


def draw_lit_blocks(block_position_x, block_position_y):
    rect = (block_position_x, block_position_y, block_size, block_size)
    pygame.draw.rect(window, yellow, rect)
    pygame.draw.rect(window, dark_grey, rect, 2)


def check_win():
    won = True
    for column in range((window_width - menu_size) // block_size):
        for row in range(len(maze_field)):
            if maze_field[row][column] == "empty_block":
                continue
            elif isinstance(maze_field[row][column], int):
                if maze_field[row][column] > 0:
                    continue
            elif isinstance(maze_field[row][column], list):
                if maze_field[row][column][1] == 0:
                    continue
            won = False
            break

    if won:  # Can be changed to whatever is desired
        print("You won in " + turn_counter + " turns!")
        reset_game()


def reset_game():
    global turn_counter
    turn_counter = 0
    for column in range((window_width - menu_size) // block_size):
        for row in range(len(maze_field)):
            if isinstance(maze_field[row][column], int):
                maze_field[row][column] = 0
    pygame.display.update()
    window.fill(dark_grey)

window.fill(dark_grey)
is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSEBUTTON:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < window_width - menu_size:
                update_light_source(mouse_x - (mouse_x % 30), mouse_y - (mouse_y % 30), turn_light_on)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_MOUSEBUTTON:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < window_width - menu_size:
                update_light_source(mouse_x - (mouse_x % 30), mouse_y - (mouse_y % 30), turn_light_off)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if reset_button_rect.collidepoint(event.pos):
                reset_game()
        draw_field()
    pygame.display.update()
    check_win()

print(maze_field)  # for debugging field
pygame.quit()
