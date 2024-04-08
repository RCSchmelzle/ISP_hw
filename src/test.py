import scipy
import skimage
import skimage.io 
import matplotlib.pyplot as plt
import numpy as np

# Config
img_path='data/baby.tiff'
wb_method='gray' # White Balance method: gray, white, preset

# 1.1.a Reconnaissance run
black = 0
white = 16383
r_scale: 1.628906
g_scale: 1.000000
b_scale: 1.386719

# 1.1.b Identify the Python Initials

# Load in the tiff
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

bayer_pattern = bayer_id(img)


# 1.1.e White Balancing
def white_balance(img, pattern, method="gray", rgb_weights=[1.0, 1.0, 1.0]):
    if method=='gray':

        TO DO: Check Greens only count once
        if pattern=='gbrg' or pattern=='grbg':
            g_mean=(img[0::2, 0::2].mean() + img[1::2, 1::2].mean())/2
        else:
            g_mean=(img[1::2, 0::2].mean() + img[0::2, 1::2].mean())/2
        if pattern=='grbg':
            r_mean=img[0::2, 1::2].mean()
            b_mean=img[1::2, 0::2].mean()
        elif pattern=='gbrg':
            b_mean=img[0::2, 1::2].mean()
            r_mean=img[1::2, 0::2].mean()
        elif pattern=='bggr':
            b_mean=img[0::2, 0::2].mean()
            r_mean=img[1::2, 1::2].mean()
        elif pattern=='rggb':
            r_mean=img[0::2, 0::2].mean()
            b_mean=img[1::2, 1::2].mean()

        rgb_weights=[r_mean, r_mean/g_mean, r_mean/b_mean]
    elif method=='white':
        TO DO 
        Calculate Weights

    elif method=='presets': # camera presets
        print('White balance using presets')
        
    # Set Greens
    if pattern=='gbrg' or pattern=='grbg':
        img[0::2, 0::2]*=rgb_weights[1]
        img[1::2, 1::2]*=rgb_weights[1]
    else:
        img[1::2, 0::2]*=rgb_weights[1]
        img[0::2, 1::2]*=rgb_weights[1]
    
    # Set Reds and Blues
    if pattern=='grbg':
        img[0::2, 1::2]*=rgb_weights[0]
        img[1::2, 0::2]*=rgb_weights[2]
    elif pattern=='gbrg':
        img[0::2, 1::2]*=rgb_weights[2]
        img[1::2, 0::2]*=rgb_weights[0]
    elif pattern=='bggr':
        img[0::2, 0::2]*=rgb_weights[2]
        img[1::2, 1::2]*=rgb_weights[0]
    elif pattern=='rggb':
        img[0::2, 0::2]*=rgb_weights[0]
        img[1::2, 1::2]*=rgb_weights[2]

white_balance(img, bayer_pattern, method=wb_method, \
               rgb_weights=[r_scale, g_scale, b_scale])