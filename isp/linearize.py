import numpy as np


# 1.1.c. Linearization
def linearize_image(img, black=0, white=16383):
    img = (img-black)/(white-black)
    img = np.clip(img, 0, 1)
    return img
