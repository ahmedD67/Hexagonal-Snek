# Example file showing a circle moving on screen
import pygame
import numpy as np
import math
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
_side = 20
x_steps = screen.get_width() // _side
y_steps = math.ceil(screen.get_height() / (_side * np.sin(np.pi / 3))) + 1


def gen_hexagon(center: pygame.Vector2 = None, side: int = None):
    if center is None:
        center = pygame.Vector2(0,0)
    if side is None:
        side = 20
    sides = [
        center +
        side * pygame.Vector2(np.cos(angle), np.sin(angle))
        for angle in np.linspace(0, (5/6) * 2*np.pi, 6)
    ]
    return sides


def gen_grid(side: int = None):
    if side is None:
        side = 20
    print(x_steps)
    print(y_steps)
    # start from top right corner of screen
    # move right and down
    for row in range(0, y_steps):
        for col in range(0, x_steps):
            if row % 2 == 0:
                _offset = 0
            else:
                _offset = 1.5

            _hex_outer = gen_hexagon(
                center=side * pygame.Vector2(3 * col + _offset, row * np.sin(np.pi/3)),
                side=side
            )
            _hex_inner = gen_hexagon(
                center=side * pygame.Vector2(3 * col + _offset, row * np.sin(np.pi/3)),
                side=0.8 * side
            )
            pygame.draw.polygon(surface=screen, color='black', points=_hex_outer, )
            pygame.draw.polygon(surface=screen, color='gray', points=_hex_inner, )


screen.fill("purple")
# gen_grid()
gen_grid(_side)
while running:
    # this array should contain the (row, col) positions of the snake
    snake_arr = [(31, 20), (33, 20), (35, 20)]

    blob_collected = True
    if blob_collected:
        # randomly select blob point
        _rand_row = np.random.randint(0,y_steps)
        _rand_col = np.random.randint(0,x_steps)

        _color = pygame.Color(255 * np.random.random(size=(3,)))

        # draw the random blob
        if _rand_row % 2 == 0:
            _offset = 0
        else:
            _offset = 1.5

        center = _side * pygame.Vector2(3 * _rand_col + _offset, _rand_row * np.sin(np.pi / 3))
        blob_hex = gen_hexagon(
            center=center,
            side=0.8*_side
        )
        pygame.draw.polygon(surface=screen, color=_color, points=blob_hex, )
        blob_collected = False

    # poll for events

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fill the screen with a color to wipe away anything from last frame



    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000


pygame.quit()