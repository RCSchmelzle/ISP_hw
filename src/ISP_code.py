import scipy
import skimage
import skimage.io 
import matplotlib.pyplot as plt
import numpy as np

# Config
img_path='data/baby.tiff'
wb_methods=['gray'] #Options: 'preset', 'gray', 'white', 'manual'

# For 'manual' white balance, here are some predefined patches
# selected_coordinates==-1 will go through all candidate coordinate
# otherwise it indexes in

candidate_coordinates=[ 
    # [190, 3279],    # Window Glare
    # [420, 3658],    # Window Glare
    # [1082, 2442],   # Baby Eye
    [937, 2559],    # Baby Eyebrow
    # [2214, 1360],   # Baby Shirt White Part
    # [1035, 1833]    # Baby Eye Glint
]
selected_coordinates=-1 


 # 1.1.a Reconnaissance Run Results
black=0
white=16383
r_scale=1.628906
g_scale=1.000000
b_scale=1.386719

# 1.1.b Identify the Python Initials
# Load in the tiff
img = skimage.io.imread(img_path, plugin='pil')

# Display the width, height, bits per pixel
print(f'Width: {img.shape[1]}')
print(f'Height: {img.shape[0]}')
print(f'Bits per Pixel: {img.dtype.name[-2:]}')

# Convert to double precision
img = img.astype('double')


# Function Definitions:
# 1.1.c. Linearization
def linearize_image(img):
    img = (img-black)/(white-black)
    img = np.clip(img, 0, 1)
    return img

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

# # 1.1.e White Balancing
# Note: I implemented two forms; one where you white balance before demosaicing, and one after
#       They should yield the same results (e.g. the means and max stay the same), but the 
#       post-demosaicing white balance is faster and cleaner to read

def wb_pre_demosaic(img, pattern, method="gray", rgb_weights=[1.0, 1.0, 1.0], coordinates=[None]):
    # To generalize to different bayer patterns, we store where the
    #  colors appear in each pattern  as that temp and use those to
    #  modify indexing (e.g. for grbg, Red is at [0,1], G starts at [0,0] and [1,1], 
    #  B starts at [1,0]) and repeat every other pixel

    if   pattern=='grbg':   temp = [0,1,0,0,1,1,1,0]
    elif pattern=='gbrg':   temp = [1,0,0,0,1,1,0,1]
    elif pattern=='bggr':   temp = [1,1,1,0,0,1,0,0]
    elif pattern=='rggb':   temp = [0,0,1,0,0,1,1,1]
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
    if   pattern=='grbg':   temp = [0,1,0,0,1,1,1,0]
    elif pattern=='gbrg':   temp = [1,0,0,0,1,1,0,1]
    elif pattern=='bggr':   temp = [1,1,1,0,0,1,0,0]
    elif pattern=='rggb':   temp = [0,0,1,0,0,1,1,1]
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

def color_space_correction(img, xyz2cam,rgb2xyz):
    rgb2cam=np.matmul(xyz2cam, rgb2xyz)
    for row in range(rgb2cam.shape[0]):
        rgb2cam[row]/=rgb2cam[row].sum()

    rgb2cam = np.linalg.inv(rgb2cam)

    for i in range(img.shape[0]):
        # print(i)
        for j in range(img.shape[1]):
            rgb=np.expand_dims(img[i,j], axis=1)
            img[i,j]=np.matmul(rgb2cam, rgb).T
    return img


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

# Full Pipeline
def isp_pipeline(img, wb_method, r_scale=1.0, g_scale=1.0, b_scale=1.0, coordinate=None):
    img=linearize_image(img)
    bayer_pattern = bayer_id(img)    
    img=wb_pre_demosaic(img, bayer_pattern, method=wb_method, rgb_weights=[r_scale, g_scale, b_scale], coordinates=coordinate)
    img = demosaic(img, bayer_pattern)

    # Can alternatively comment out the wb_pre_demosaic and do below for improved speed
    # img=wb_post_demosaic(img, method=wb_method, rgb_weights=[r_scale, g_scale, b_scale], coordinates=coordinate)


    rgb2xyz = np.array([[0.4124564, 0.3575761, 0.1804375],
                        [0.2126729, 0.7151522, 0.0721750],
                        [0.0193339, 0.1191920, 0.9503041]])
    
    xyz2cam = np.array([6988,-1384,-714,-5631,13410,2447,-1485,2204,7318]).reshape(3, 3, order='C')/10000

    img=color_space_correction(img, xyz2cam,rgb2xyz)        
    img=brightness_adj(img, target_mean=0.55)

    skimage.io.imsave(f"../image_{wb_method}_{coordinate}.png", (img*255).astype('uint8'))
    skimage.io.imsave(f"../image_{wb_method}_{coordinate}_95.jpg", (img*255).astype('uint8'), quality=95)


# Run all different variants
for wb_method in wb_methods:
    if wb_method=='manual':
        manual_coordinates=candidate_coordinates
        if selected_coordinates!=-1:
            manual_coordinates=[candidate_coordinates[selected_coordinates]]
    else:
        manual_coordinates=[None]

    for coordinate in manual_coordinates:
        isp_pipeline(img, wb_method, r_scale=r_scale, g_scale=g_scale, b_scale=b_scale, coordinate=coordinate)