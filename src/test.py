import scipy
import skimage
import skimage.io 
import matplotlib.pyplot as plt
import numpy as np


# 1.1.a Reconnaissance run
black = 0
white = 16383

# 1.1.b Identify the Python Initials

# Load in the tiff
img_path='data/baby.tiff'
img = skimage.io.imread(img_path, plugin='pil')

# Display the width, height, bits per pixel
print(f'Width: {img.shape[1]}')
print(f'Height: {img.shape[0]}')
print(f'Bits per Pixel: {img.dtype.name[-2:]}')

# Convert to double precision
img = img.astype('double')

# 1.1.c. Linearization
img = (img-black)/(white-black)
img = np.clip(img, 0, 1)

# 1.1.d. Bayer Pattern Identification
def bayer_id(img):
    # Given that light is scattering over the sensors
    # likely at a similar wavelength for the adjacent pixels
    # colors that are closer in wavelength will have a similar 
    # response to the light, so:
    #   To find greens, look for the most similar diagonal
    #   To find blue, find which of the remaining pixels is most similar 

    pattern=img[:2, :2]
    if abs(pattern[0,0] - pattern[1,1]) < abs(pattern[0,1] - pattern[1,0]):
        # Gs are [0,0], [1,1]
        avg_g = (pattern[0,0] + pattern[1,1])/2
        if (abs(avg_g-pattern[0,1]) < abs(avg_g-pattern[1,0])):
            pattern='gbrg' # B is at [0,1]
        else:
            pattern='grbg' # B is at [1,0]
    else: # Gs are [0,1], [1,0]
        avg_g = (pattern[0,1] + pattern[1,0])/2
        if (abs(avg_g-pattern[0,0]) < abs(avg_g-pattern[1,1])):
            pattern='bggr' # B is at [0,0]
        else:
            pattern='rggb' # B is at [1,1]
    return pattern





bayer_id(img)