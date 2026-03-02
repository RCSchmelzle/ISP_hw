import numpy as np

# Bayer pattern index mapping:
# [r1, r2, g1, g2, g3, g4, b1, b2]
# For each pattern, these define the start row,col indices for
# R, G (two sites), and B channels in the 2x2 repeating tile
BAYER_PATTERNS = {
    'grbg': [0, 1, 0, 0, 1, 1, 1, 0],
    'gbrg': [1, 0, 0, 0, 1, 1, 0, 1],
    'bggr': [1, 1, 1, 0, 0, 1, 0, 0],
    'rggb': [0, 0, 1, 0, 0, 1, 1, 1],
}


# 1.1.d. Bayer Pattern Identification
def bayer_id(img):
    # Given that light is scattering over the sensors
    # likely at a similar wavelength for the adjacent pixels
    # colors that are closer in camera sensor spectrum will have a similar
    # response to the light; based on this logic and the example spectra from
    # the slides:
    #   To find greens, look for the most similar entries on a diagonal
    #   To find blue, find which of the remaining pixels is most similar
    #       to the greens

    # Take a snippet of 2x2 to evaluate the pattern
    pattern=img[:2, :2]

    # See which diagonal is more similar; these are greens
    if abs(pattern[0,0] - pattern[1,1]) < abs(pattern[0,1] - pattern[1,0]):
        # Gs are [0,0], [1,1]
        avg_g = (pattern[0,0] + pattern[1,1])/2

        # Find which remaining pixel is more similar to greens, these are blue
        if (abs(avg_g-pattern[0,1]) < abs(avg_g-pattern[1,0])):
            pattern='gbrg' # B is at [0,1]
        else:
            pattern='grbg' # B is at [1,0]
    else: # Gs are [0,1], [1,0]
        avg_g = (pattern[0,1] + pattern[1,0])/2

        # Find which remaining pixel is more similar to greens, these are blue
        if (abs(avg_g-pattern[0,0]) < abs(avg_g-pattern[1,1])):
            pattern='bggr' # B is at [0,0]
        else:
            pattern='rggb' # B is at [1,1]
    return pattern
