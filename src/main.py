import numpy as np
import pygame
from perlin_numpy import generate_fractal_noise_3d
from color import COLOR_PALETTE
from fire import *


s = 5
W,H,SCALE = 3840//s, 2160//s, s
RATE = 30

pygame.init()
screen = pygame.display.set_mode((W*SCALE, H*SCALE))
surface = pygame.Surface((W,H))
clock = pygame.time.Clock()


fire_state = np.zeros((W+2*EDGE,H+HEIGHT), dtype=np.uint8)
pixels = np.zeros((W,H,3), dtype=np.uint8)
rng = np.random.default_rng()
cols = np.arange(EDGE, W + EDGE)

T = 240
noise = generate_fractal_noise_3d((T, W, HEIGHT), (4, 3, 1), tileable=(True, False, False))
noise = (noise - noise.min()) / (noise.max() - noise.min())
FIRE_STARTERS = np.round(MIN_STARTING_FIRE + noise * (MAX_STARTING_FIRE - MIN_STARTING_FIRE)).astype(np.uint8)

fire_on = True
timestep = 0


def work_fire():
    global fire_on
    fire_on = True

    fire_state[EDGE:W+EDGE, -1-HEIGHT:-1] = FIRE_STARTERS[timestep]


def stop_fire():
    global fire_on
    fire_on = False

    fire_state[EDGE:W+EDGE, -1-HEIGHT:-1] = np.zeros((W,HEIGHT))


def update_fire_state():

    for i in range(0, H):

        # propagate fire upwards and to the sides
        rc = np.trunc(np.random.randint(-10*WINDINESS, 10*WINDINESS+1, cols.size) / 10).astype(np.intp)
        rh = np.floor(np.random.randint(10, 10*HEIGHT+1, cols.size)/10).astype(np.intp)
        fire_state[EDGE:W+EDGE, i] = fire_state[cols+rc, i+rh]

        # add some decay
        fire_state[:, i] -= np.clip(rng.normal(1, 2, W+2*EDGE), 0, fire_state[:, i]).astype(np.uint8)


def update_pixels():
    pixels[:] = COLOR_PALETTE[fire_state[EDGE:-EDGE, :-HEIGHT]]


running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                if fire_on:
                    stop_fire()
                else:
                    work_fire()

    if fire_on:
        work_fire()
    timestep += 1
    timestep %= T

    update_fire_state()
    update_pixels()
    
    pygame.surfarray.blit_array(surface, pixels)
    pygame.transform.scale(surface, screen.get_size(), screen)
    pygame.display.flip()

    clock.tick(RATE)


