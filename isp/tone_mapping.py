import numpy as np
import skimage.color


def brightness_adj(img, target_mean=0.5):
    # Linear Scaling
    scale=target_mean/skimage.color.rgb2gray(img).mean()
    img*=scale
    img=np.clip(img, 0,1)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for c in range(3):
                if img[i,j,c] <= 0.0031308:
                    img[i,j,c]*=12.92
                else:
                    img[i,j,c]=(1+0.055)*(img[i,j,c]**(1/2.4))-0.055


    return img
