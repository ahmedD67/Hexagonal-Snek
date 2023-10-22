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
_side = 30
print(screen.get_width())
x_steps = screen.get_width() // _side  # Haven't figured out why yet, number of visible columns caps at 43
y_steps = screen.get_height() // _side

def gen_grid(side: int = None):
    if side is None:
        side = 20
    # start from top right corner of screen
    # move right and down
    for row in range(0, y_steps):
        for col in range(0, x_steps):
            pygame.draw.rect(surface=screen, color='black', rect=(row*side, col*side, (row + 1) * side, (col + 1) * side), width=int(0.1*side))


screen.fill("gray")
# gen_grid()
blob_collected = True
_rand_row = np.random.randint(0, y_steps)
_rand_col = np.random.randint(0, x_steps)
snake_arr = [(2, 5), (2, 6), (2, 7)]

up_dir = True
right_dir = None

while running:
    print(x_steps)
    print(y_steps)
    gen_grid(_side)
    # this array should contain the (row, col) positions of the snake

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        right_dir = False
        up_dir = None
    elif keys[pygame.K_d]:
        right_dir = True
        up_dir = None
    elif keys[pygame.K_w]:
        right_dir = None
        up_dir = True
    elif keys[pygame.K_s]:
        right_dir = None
        up_dir = False

    # snake_arr[0] = (snake_arr[0][0] % 22, snake_arr[0][1] % 43)

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
    elif up_dir is None and right_dir:  # just right
        _new_row = snake_arr[0][0]
        _new_col = snake_arr[0][1] + 1
        snake_arr.insert(0, (_new_row, _new_col))
        snake_arr.pop()
    elif up_dir is None and not right_dir:  # just left
        _new_row = snake_arr[0][0]
        _new_col = snake_arr[0][1] - 1
        snake_arr.insert(0, (_new_row, _new_col))
        snake_arr.pop()

    for pt in snake_arr:
        # alphas = np.linspace(0.5, 0.9, len(snake_arr))
        print(snake_arr)
        side = _side
        row, col = pt
        pygame.draw.rect(surface=screen, color=(0, 101, 0), rect=(row * side + 0.1 * side, col * side + 0.1 * side,
                                                                      (row + 1) * side - 0.1 * side,
                                                                      (col + 1) * side - 0.1 * side), )
        # pygame.draw.polygon(surface=screen, color=(0,101,0), points=pt_hex, )

    blob_collected = snake_arr[0] == (_rand_row, _rand_col)

    if not blob_collected:
        # randomly select blob point

        pygame.draw.rect(surface=screen, color=(0, 101, 0), rect=(_rand_row * _side + 0.1 * _side, _rand_col * _side + 0.1 * _side,
                                                                  (_rand_row + 1) * _side - 0.1 * _side,
                                                                  (_rand_col + 1) * _side - 0.1 * _side), )

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
    dt = clock.tick(5) / 1000


pygame.quit()