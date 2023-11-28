import pygame
import pandas as pd

pygame.init()
maze_name = "lights-small-1.csv"
maze_dir = ("lights-puzzles\\" + maze_name)

white = (255, 255, 255)
dark_grey = (25, 25, 25)
yellow = (255, 255, 0)

block_size = 30
font = pygame.font.Font(None, 36)
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

global block_position_x, block_position_y
block_position_x = 0
block_position_y = 0


def draw_block(block_position_x, block_position_y):
    rect = (block_position_x, block_position_y, block_size, block_size)
    pygame.draw.rect(window, white, rect)
    pygame.draw.rect(window, dark_grey, rect, 2)

def draw_field():
    global block_position_x, block_position_y
    df = pd.read_csv(maze_dir, header=None, sep=";")
    for row_letter in range(len(df)):
        for column_letter in range(len(df[row_letter])):
            if df.isnull()[row_letter][column_letter]:
                draw_block(block_position_x, block_position_y)
                block_position_x += 40
                if block_position_x == window_width:
                    block_position_x = 0
                    block_position_y += 40
            else:
                print(df[row_letter][column_letter])


is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

    #window.fill(dark_grey)
    draw_field()

    pygame.display.flip()

pygame.quit()
