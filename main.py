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
x_steps = screen.get_width() // (2 * _side)
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
blob_collected = True
_rand_row = np.random.randint(0,y_steps)
_rand_col = np.random.randint(0,x_steps)
snake_arr = [(5, 1), (6, 1), (7, 1)]

up_dir = True
right_dir = None

while running:
    gen_grid(_side)
    # this array should contain the (row, col) positions of the snake

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        right_dir = False
    elif keys[pygame.K_d]:
        right_dir = True
    elif keys[pygame.K_w]:
        up_dir = True
        right_dir = None
    elif keys[pygame.K_s]:
        up_dir = False
        right_dir = None

    if up_dir and right_dir is None:
        _new_row = snake_arr[0][0] - 2
        _new_col = snake_arr[0][1]
        snake_arr.insert(0, (_new_row, _new_col))
        snake_arr.pop()
    elif not up_dir and right_dir is None:
        _new_row = snake_arr[0][0] + 2
        _new_col = snake_arr[0][1]
        snake_arr.insert(0, (_new_row, _new_col))
        snake_arr.pop()
    elif up_dir and right_dir:
        _new_row = snake_arr[0][0] - 1
        _new_col = snake_arr[0][1] + 1
        snake_arr.insert(0, (_new_row, _new_col))
        snake_arr.pop()
    elif not up_dir and right_dir:
        _new_row = snake_arr[0][0] + 1
        _new_col = snake_arr[0][1] + 1
        snake_arr.insert(0, (_new_row, _new_col))
        snake_arr.pop()
    elif up_dir and not right_dir:
        _new_row = snake_arr[0][0] - 1
        _new_col = snake_arr[0][1] - 0
        snake_arr.insert(0, (_new_row, _new_col))
        snake_arr.pop()
    elif not up_dir and not right_dir:
        _new_row = snake_arr[0][0] + 1
        _new_col = snake_arr[0][1] - 0
        snake_arr.insert(0, (_new_row, _new_col))
        snake_arr.pop()

    for pt in snake_arr:
        print(snake_arr)
        if pt[0] % 2 == 0:
            _offset = 0
        else:
            _offset = 1.5

        center = _side * pygame.Vector2(3 * pt[1] + _offset, pt[0] * np.sin(np.pi / 3))
        pt_hex = gen_hexagon(
            center=center,
            side=0.8 * _side
        )
        pygame.draw.polygon(surface=screen, color="blue", points=pt_hex, )

    if blob_collected:
        # randomly select blob point
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
        # pygame.draw.polygon(surface=screen, color=_color, points=blob_hex, )
        pygame.draw.polygon(surface=screen, color="red", points=blob_hex, )
        blob_collected = False

    # poll for events

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(20) / 1000


pygame.quit()