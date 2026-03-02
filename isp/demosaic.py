import numpy as np

from .bayer import BAYER_PATTERNS


# 1.1.f Demosaicing
def channel_interp(array, threshold=0):
    # Other interpolation functions (e.g. interpolate, interp2D) gave errors that too much of
    # the image was missing, so I implemented myself
    # Interpolates when colors are below a threshold (e.g. data==-1)
    array[array<threshold] = np.nan
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if np.isnan(array[i,j]):
                neighbor_avg=0
                neighbors=0
                if j>0 and not np.isnan(array[i,j-1]):
                    neighbors+=1
                    neighbor_avg+=array[i,j-1]
                if j<(array.shape[1]-1) and not np.isnan(array[i,j+1]):
                    neighbors+=1
                    neighbor_avg+=array[i,j+1]
                if i>0 and not np.isnan(array[i-1,j]):
                    neighbors+=1
                    neighbor_avg+=array[i-1,j]
                if i<(array.shape[0]-1) and not np.isnan(array[i+1,j]):
                    neighbors+=1
                    neighbor_avg+=array[i+1,j]
                if neighbors==0: continue
                neighbor_avg/=neighbors
                array[i,j]=neighbor_avg

    return array

def bilinear_interp(array):
        array=channel_interp(array, 0.0)
        array=channel_interp(array, 0.0)
        return array

def demosaic(img, pattern):
    r_channel = np.full(img.shape, -1, img.dtype)
    g_channel = np.full(img.shape, -1, img.dtype)
    b_channel = np.full(img.shape, -1, img.dtype)

    # Set the start indices for the grid pattern
    temp = BAYER_PATTERNS[pattern]
    [r1,r2,g1,g2,g3,g4,b1,b2] = temp

    r_channel[r1::2, r2::2]=img[r1::2, r2::2]
    g_channel[g1::2, g2::2]=img[g1::2, g2::2]
    g_channel[g3::2, g4::2]=img[g3::2, g4::2]
    b_channel[b1::2, b2::2]=img[b1::2, b2::2]

    r_channel=bilinear_interp(r_channel)
    g_channel=bilinear_interp(g_channel)
    b_channel=bilinear_interp(b_channel)
    rgb_img = np.zeros((r_channel.shape[0], r_channel.shape[1], 3))

    rgb_img[:,:,0]=r_channel
    rgb_img[:,:,1]=g_channel
    rgb_img[:,:,2]=b_channel

    return rgb_img
