import numpy as np
from fire import MAX_STARTING_FIRE


def make_palette(n, n_stops=4):
    t = np.linspace(0, 1, n)
    stops = np.linspace(0, 1, n_stops)
    r = np.interp(t, stops, [0, 255, 240, 240])
    g = np.interp(t, stops, [0,   0, 240, 240])
    b = np.interp(t, stops, [0,   0,   0, 240])
    return np.stack([r, g, b], axis=-1).astype(np.uint8)


COLOR_PALETTE = make_palette(MAX_STARTING_FIRE + 1)

