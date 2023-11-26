import pygame

pygame.init()

window_width = 600
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Lights")

white = (255, 255, 255)
dark_grey = (25, 25, 25)
yellow = (255, 255, 0)

font = pygame.font.Font(None, 36)

is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

    window.fill(dark_grey)

    pygame.display.flip()

pygame.quit()
