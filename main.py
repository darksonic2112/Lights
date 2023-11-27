import pygame
import pandas as pd

pygame.init()
maze_field = "lights-puzzles-small\\lights-small-1.csv"

# Small size field: 14x14 blocks
# Mid-size field: 25x25 blocks
# Blocks are 40x40 px
window_width = 1000
window_height = 1000
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Lights")

white = (255, 255, 255)
dark_grey = (25, 25, 25)
yellow = (255, 255, 0)
font = pygame.font.Font(None, 36)

df = pd.read_csv(maze_field, header=None, sep=";")
print(df[1][0])


def draw_rect():
    pass


rect = (0, 0, 40, 40)

is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

    window.fill(dark_grey)
    pygame.draw.rect(window, white, rect)
    pygame.draw.rect(window, dark_grey, rect, 2)

    pygame.display.flip()

pygame.quit()
