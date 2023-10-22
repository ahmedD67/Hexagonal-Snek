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
print(screen.get_width())
x_steps = 44  # screen.get_width() // _side  # Haven't figured out why yet, number of visible columns caps at 43
y_steps = math.ceil(screen.get_height() / (2 * _side * np.sin(np.pi / 3))) + 1


def gen_hexagon(center: pygame.Vector2 = None, side: float = None):
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


def gen_center(row, col):
    if col % 2 == 0:
        return _side * pygame.Vector2(1.5 * col, 2 * row * np.sin(np.pi / 3))
    else:
        return _side * pygame.Vector2(1.5 * col, 2 * row * np.sin(np.pi / 3) + np.sin(np.pi / 3))


def gen_grid(side: int = None):
    if side is None:
        side = 20
    # start from top right corner of screen
    # move right and down
    for row in range(0, y_steps):
        for col in range(0, x_steps):
            if col % 2 == 0:
                _hex_outer = gen_hexagon(
                    center=gen_center(row, col),
                    side=side
                )
                _hex_inner = gen_hexagon(
                    center=gen_center(row, col),
                    side=0.8 * side
                )
            else:
                _hex_outer = gen_hexagon(
                    center=gen_center(row, col),
                    side=side
                )
                _hex_inner = gen_hexagon(
                    center=gen_center(row, col),
                    side=0.8 * side
                )

            pygame.draw.polygon(surface=screen, color='black', points=_hex_outer, )
            pygame.draw.polygon(surface=screen, color=(255, 255, 208), points=_hex_inner, )


screen.fill("purple")
# gen_grid()
blob_collected = True
_rand_row = np.random.randint(0, y_steps)
_rand_col = np.random.randint(0, x_steps)
snake_arr = [(5, 1), (6, 1), (7, 1)]

up_dir = True
right_dir = None

bg = pygame.image.load("images/background_grid.png")
while running:
    print(x_steps)
    print(y_steps)

    # INSIDE OF THE GAME LOOP
    screen.blit(bg, (0, 0))
    # this array should contain the (row, col) positions of the snake

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        right_dir = False
    elif keys[pygame.K_d]:
        right_dir = True
    elif keys[pygame.K_w]:
        if right_dir is None:
            pass
        else:
            up_dir = True
            right_dir = None

    elif keys[pygame.K_s]:
        if right_dir is None:
            pass
        else:
            up_dir = False
            right_dir = None

    snake_arr[0] = (snake_arr[0][0] % 22, snake_arr[0][1] % 43)

    if snake_arr[0] in snake_arr[1:]:
        exit()

    if up_dir and right_dir is None:  # just up
        _new_row = snake_arr[0][0] - 1
        _new_col = snake_arr[0][1]
        snake_arr.insert(0, (_new_row, _new_col))
        snake_arr.pop()
    elif not up_dir and right_dir is None:  # just down
        _new_row = snake_arr[0][0] + 1
        _new_col = snake_arr[0][1]
        snake_arr.insert(0, (_new_row, _new_col))
        snake_arr.pop()
    elif up_dir and right_dir:  # up and right
        _new_col = snake_arr[0][1] + 1
        if snake_arr[0][1] % 2 == 0:
            _new_row = snake_arr[0][0] - 1
        else:
            _new_row = snake_arr[0][0]
        snake_arr.insert(0, (_new_row, _new_col))
        snake_arr.pop()
    elif not up_dir and right_dir:  # down and right
        _new_col = snake_arr[0][1] + 1
        if snake_arr[0][1] % 2 == 0:
            _new_row = snake_arr[0][0]
        else:
            _new_row = snake_arr[0][0] + 1
        snake_arr.insert(0, (_new_row, _new_col))
        snake_arr.pop()
    elif up_dir and not right_dir:  # up and left
        _new_col = snake_arr[0][1] - 1
        if snake_arr[0][1] % 2 == 0:
            _new_row = snake_arr[0][0] - 1
        else:
            _new_row = snake_arr[0][0]
        snake_arr.insert(0, (_new_row, _new_col))
        snake_arr.pop()
    elif not up_dir and not right_dir:  # down and left
        _new_col = snake_arr[0][1] - 1
        if snake_arr[0][1] % 2 == 0:
            _new_row = snake_arr[0][0]
        else:
            _new_row = snake_arr[0][0] + 1
        snake_arr.insert(0, (_new_row, _new_col))
        snake_arr.pop()


    for pt in snake_arr:
        # alphas = np.linspace(0.5, 0.9, len(snake_arr))
        center = gen_center(pt[0], pt[1])
        pt_hex = gen_hexagon(
            center=center,
            side=0.8 * _side
        )
        pygame.draw.polygon(surface=screen, color=(0,101,0), points=pt_hex, )

    blob_collected = snake_arr[0] == (_rand_row, _rand_col)

    if not blob_collected:
        # randomly select blob point

        blob_hex = gen_hexagon(
            center=gen_center(_rand_row, _rand_col),
            side=0.8 * _side
        )

        # draw the random blob
        # pygame.draw.polygon(surface=screen, color=_color, points=blob_hex, )
        pygame.draw.polygon(surface=screen, color="purple", points=blob_hex, )
    else:
        _rand_row = np.random.randint(1, 21)
        _rand_col = np.random.randint(1, 43)

        snake_arr.append(
            (snake_arr[-1][0] + 1, snake_arr[-1][1])
        )
    print(blob_collected)
    print(snake_arr[0])
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
    dt = clock.tick(60) / 1000


pygame.quit()