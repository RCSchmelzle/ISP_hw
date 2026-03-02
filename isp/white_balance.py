import numpy as np

from .bayer import BAYER_PATTERNS


# # 1.1.e White Balancing
# Note: I implemented two forms; one where you white balance before demosaicing, and one after
#       They should yield the same results (e.g. the means and max stay the same), but the
#       post-demosaicing white balance is faster and cleaner to read

def wb_pre_demosaic(img, pattern, method="gray", rgb_weights=[1.0, 1.0, 1.0], coordinates=[None]):
    # To generalize to different bayer patterns, we store where the
    #  colors appear in each pattern  as that temp and use those to
    #  modify indexing (e.g. for grbg, Red is at [0,1], G starts at [0,0] and [1,1],
    #  B starts at [1,0]) and repeat every other pixel

    temp = BAYER_PATTERNS[pattern]
    [r1,r2,g1,g2,g3,g4,b1,b2] = temp

    if method=='gray':

        # assume the image averages to a gray (e.g. r, g, and b have equal averages)
        # and scale.
        r_mean=img[r1::2, r2::2].mean()
        g_mean=(img[g1::2, g2::2].mean() + img[g3::2, g4::2].mean())/2
        b_mean=img[b1::2, b2::2].mean()

        mean_max=max(r_mean, g_mean, b_mean)
        rgb_weights=[0.5/r_mean, 0.5/g_mean, 0.5/b_mean]
        # Note, it was not specified if gray=0.5, just that they are a gray
        # and therefore equal; if we want gray to equal 0.5, then we add an extra line
        # rgb_weights=0.5/rgb_weights
        print('White balance using gray world assumption')
    elif method=='white':
        # Variation 1:
        # Go over each "pixel" (as it is not demosaiced, we look at each group of 4)
        # the one with the highest brightness is white, use that to rescale
        max_brightness=0
        for i in range(0,img.shape[0]-1, 2):
            for j in range(0,img.shape[1]-1, 2):
                r_curr=img[i+r1, j+r2]
                g1_curr=img[i+g1, j+g2]
                g2_curr=img[i+g3, j+g4]
                b_curr=img[i+b1, j+b2]

                # Get the sum of the pixel values to determine the brightness (but average greens as that pixel will be dimmer)
                curr_brightness=r_curr+max(g1_curr,g2_curr)+b_curr
                if curr_brightness > max_brightness:
                    max_brightness=curr_brightness
                    curr_max=[r_curr, max(g1_curr, g2_curr), b_curr]


        # Variant 2: Just rescale to the max brightness of each channel, doesn't matter where or if they're in the same place
        # r_max=img[r1::2, r2::2].max()
        # g_max=max(img[g1::2, g2::2].max(), img[g3::2, g4::2].max())
        # b_max=img[b1::2, b2::2].max()
        # rgb_weights=[1/r_max, 1/g_max, 1/b_max]

        # Variant 3: Rescale all to just use the max overall
        # max=img.max()
        # rgb_weights=[1/max, 1/max, 1/max]


        print('White balance using white world assumption')

        #   Note: when discussing this in OH, it wasn't totally clear, so I went with the above implementation
        #       (e.g. find what will become the brightest pixel in the scene and use that to rescale)
        #       based on the OH discussion. This won't necessarily yield a single white pixel but the brightest instance of each channel
        #       from across the image.

    elif method=='presets': # camera presets fed in as weights
        print('White balance using presets')

    elif method=='manual': # select a coordinate to treat as white
        # Set the white balance to be the top corner of the bayer pattern
        coordinates[0]-=(coordinates[0]%2)
        coordinates[1]-=(coordinates[1]%2)

        # Get the values from the bayer pattern of the selected pixel
        r_curr=img[coordinates[0]+r1, coordinates[0]+r2]
        g_curr=(img[coordinates[0]+g1, coordinates[0]+g2]+img[coordinates[0]+g3, coordinates[0]+g4])/2
        b_curr=img[coordinates[0]+b1, coordinates[0]+b2]


        rgb_weights=[1/r_curr, 1/g_curr, 1/b_curr]
        print('White balance using manual selection')


    img[r1::2, r2::2]*=rgb_weights[0]
    img[g1::2, g2::2]*=rgb_weights[1]
    img[g3::2, g4::2]*=rgb_weights[1]
    img[b1::2, b2::2]*=rgb_weights[2]
    # img=np.clip(img, 0, 1)

    return img

def wb_post_demosaic(img, method="gray", rgb_weights=[1.0, 1.0, 1.0], coordinates=None):
    # Alternatively, we could white balance after demosaicing, which is cleaner
    # and should yield similar results
    if method=='gray':
        r_mean=img[:,:,0].mean()
        g_mean=img[:,:,1].mean()
        b_mean=img[:,:,2].mean()
        # max_mean=max(r_mean, g_mean, b_mean)
        rgb_weights=[0.5/r_mean, 0.5/g_mean, 0.5/b_mean]
        print('White balance using gray world assumption')
    elif method=='white': # get the brightest pixel (sum each channel and compare)
        white=img[np.unravel_index(np.argmax(img.sum(axis=2)), img.shape[:2])]
        rgb_weights=[1/white[0], 1/white[1], 1/white[2]]
        print('White balance using white world assumption')
    elif method=='manual': # select a pixel manually that is white
        white=img[coordinates[0], coordinates[1]]
        rgb_weights=[1/white[0], 1/white[1], 1/white[2]]
        print('White balance using manual selection')
    elif method=='presets': # camera presets fed in as weights
        print('White balance using presets')

    img[:,:,0]*=rgb_weights[0]
    img[:,:,1]*=rgb_weights[1]
    img[:,:,2]*=rgb_weights[2]
    # img=np.clip(img, 0, 1)

    return img
