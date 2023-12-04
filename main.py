import pygame
import pandas as pd

pygame.init()
#  Enter "lights1" (1-5) or "lights-small-1" (1-5) for the different mazes
maze_name = "lights-small-1.csv"
maze_dir = ("lights-puzzles\\" + maze_name)

white = (255, 255, 255)
dark_grey = (25, 25, 25)
yellow = (255, 255, 0)

# Small size field: 14x14 blocks
# Mid-size field: 25x25 blocks
# Blocks are 40x40 px
if maze_name[6] == "-":
    window_width = 420
    window_height = 420
else:
    window_width = 750
    window_height = 750
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Lights")

block_size = 30
font = pygame.font.Font(None, 30)

light_bulb = pygame.image.load("assets\\lightbulb.png")

global block_position_x, block_position_y
block_position_x = 0
block_position_y = 0

global numbers
numbers = []
for index in range(4):
    numbers.append(index)

global lit_blocks
lit_blocks = []

def get_block_at_mouse_position(mouse_x, mouse_y):
    column = mouse_x // block_size
    row = mouse_y // block_size
    return column, row


def draw_white_block(block_position_x, block_position_y):
    rect = (block_position_x, block_position_y, block_size, block_size)
    pygame.draw.rect(window, white, rect)
    pygame.draw.rect(window, dark_grey, rect, 2)
    pygame.display.flip()


def draw_dark_grey_block(block_position_x, block_position_y, number):
    number_rect = pygame.Rect(block_position_x, block_position_y, block_size, block_size)
    number_surface = font.render(number, True, white)
    number_text_rect = number_surface.get_rect()
    number_text_rect.center = number_rect.center
    pygame.draw.rect(window, dark_grey, number_rect)
    pygame.draw.rect(window, dark_grey, number_rect, 2)
    text_x = number_rect.centerx - number_text_rect.width / 2
    text_y = number_rect.centery - number_text_rect.height / 2
    window.blit(number_surface, (text_x, text_y))
    pygame.display.flip()


def draw_light(light_bulb_position_x, light_bulb_position_y):
    global lit_blocks
    window.blit(light_bulb, (light_bulb_position_x + 2, light_bulb_position_y + 3))  # +3 to get it centered
    df = pd.read_csv(maze_dir, header=None, sep=";")
    for row_letter in range(len(df)):
        for column_letter in range(len(df[row_letter])):
            #  print(df[row_letter][column_letter])
            pass
    lit_blocks.append((range(block_position_x - (block_position_x % 30), block_position_x - (block_position_x % 30) +
                             block_size),
                       range(block_position_y - (block_position_y % 30), block_position_y - (block_position_y % 30) +
                             block_size)))


def draw_field():
    global block_position_x, block_position_y, numbers
    df = pd.read_csv(maze_dir, header=None, sep=";")
    for row_letter in range(len(df)):
        for column_letter in range(len(df[row_letter])):
            if df[row_letter][column_letter] in numbers:
                number = str(int(df[row_letter][column_letter]))
                draw_dark_grey_block(block_position_x, block_position_y, number)
                block_position_x += 30
                if block_position_x == window_width:
                    block_position_x = 0
                    block_position_y += 30
            elif df.isnull()[row_letter][column_letter]:
                draw_white_block(block_position_x, block_position_y)
                block_position_x += 30
                if block_position_x == window_width:
                    block_position_x = 0
                    block_position_y += 30
            else:
                #  print(df[row_letter][column_letter])
                pass
    pygame.display.flip()


is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x and mouse_y in lit_blocks:
                print("Test")
            draw_light(mouse_x - (mouse_x % 30), mouse_y - (mouse_y % 30))

    draw_field()

    pygame.display.flip()

pygame.quit()
