import scipy
import skimage
import skimage.io 
import matplotlib.pyplot as plt
import numpy as np

# Config
img_path='data/baby.tiff'
# wb_method='white' # White Balance method: gray, white, preset
wb_methods=['white', 'gray', 'preset']

# manual_coordinates=[ None,
# [190, 3279] # Window Glare
# [420, 3658] # Window Glare
# [1082, 2442],# Baby Eye
# [937, 2559],# Baby Eyebrow
# [2214, 1360], # Baby Shirt White Part
# [1035, 1833]] # Baby Eye Glint


for wb_method in wb_methods:
# Row, Column white balance manual coordinates
    if wb_method=='white':
        manual_coordinates=[ None,
        [190, 3279], # Window Glare
        [420, 3658], # Window Glare
        [1082, 2442],# Baby Eye
        [937, 2559],# Baby Eyebrow
        [2214, 1360], # Baby Shirt White Part
        [1035, 1833]] # Baby Eye Glint

    else:
        manual_coordinates=[None]

    for coordinate in manual_coordinates:
        # 1.1.a Reconnaissance run
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
        def white_balance_premosaic(img, pattern, method="gray", rgb_weights=[1.0, 1.0, 1.0]):
            if   pattern=='grbg':   temp = [0,1,0,0,1,1,1,0]
            elif pattern=='gbrg':   temp = [1,0,0,0,1,1,0,1]
            elif pattern=='bggr':   temp = [1,1,1,0,0,1,0,0]
            elif pattern=='rggb':   temp = [0,0,1,0,0,1,1,1]
            [r1,r2,g1,g2,g3,g4,b1,b2] = temp


            if method=='gray':
                r_mean=img[r1::2, r2::2].mean()
                g_mean=(img[g1::2, g2::2].mean() + img[g3::2, g4::2].mean())/2
                b_mean=img[b1::2, b2::2].mean()

                rgb_weights=[r_mean, r_mean/g_mean, r_mean/b_mean]
                print('White balance using gray world assumption')
            elif method=='white':
                print('TODO')
            #     TO DO 
            #     Calculate Weights
                print('White balance using white world assumption')
            elif method=='presets': # camera presets
                print('White balance using presets')
                

            [r1,r2,g1,g2,g3,g4,b1,b2]  =temp
            img[r1::2, r2::2]*=rgb_weights[0]
            img[g1::2, g2::2]*=rgb_weights[1]
            img[g3::2, g4::2]*=rgb_weights[1] 
            img[b1::2, b2::2]*=rgb_weights[2]
            img=np.clip(img, 0, 1)

            

            return img

        def white_balance_postmosaic(img, method="gray", rgb_weights=[1.0, 1.0, 1.0], coordinates=None):
        

            if method=='gray':
                r_mean=img[:,:,0].mean()
                g_mean=img[:,:,1].mean() 
                b_mean=img[:,:,2].mean() 

                rgb_weights=[r_mean, r_mean/g_mean, r_mean/b_mean]
                print('White balance using gray world assumption')
            elif method=='white':
                if coordinates != None:
                    white=img[coordinates[0], coordinates[1]]
                else: 
                    white=img[np.unravel_index(np.argmax(img.sum(axis=2)), img.shape[:2])]
                
                rgb_weights=[1/white[0], 1/white[1], 1/white[2]]
                print('White balance using white world assumption')
            elif method=='presets': # camera presets
                print('White balance using presets')
                
            img[:,:,0]*=rgb_weights[0]
            img[:,:,1]*=rgb_weights[1]
            img[:,:,2]*=rgb_weights[2]
            # img=np.clip(img, 0, 1)


            return img




        # 1.1.f Demosaicing
        def channel_interp(array, threshold=0): # Interp2d was deprecated so followed this tutorial
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
                            
            # v1=False
            # if v1:
            #     array[array<0] = np.nan
            #     x = np.arange(0, array.shape[1])
            #     y = np.arange(0, array.shape[0])

            #     array = np.ma.masked_invalid(array)
            #     xx, yy = np.meshgrid(x, y)

            #     x1 = xx[~array.mask]
            #     y1 = yy[~array.mask]
            #     newarr = array[~array.mask]

            #     GD1 = scipy.interpolate.griddata((x1, y1), newarr.ravel(),
            #                             (xx, yy),
            #                                 method='linear')
            # else:
            #     array[array<0] = np.nan
            #     # Find non-NaN indices
            #     x_indices, y_indices = np.where(~np.isnan(array))

            #     # Extract non-NaN values
            #     x = x_indices.astype(float)
            #     y = y_indices.astype(float)
            #     z = array[~np.isnan(array)]

            #     # Define interpolation function using bilinear interpolation
            #     interp_func = scipy.interpolate.interp2d(x, y, z, kind='linear')

            #     # Create a meshgrid for all indices
            #     x_grid, y_grid = np.meshgrid(np.arange(array.shape[0]), np.arange(array.shape[1]))

            #     # Interpolate NaN values using bilinear interpolation
            #     GD1 = interp_func(x_grid, y_grid)

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

            def bilinear_interp(array):
                array=channel_interp(array, 0.0)
                array=channel_interp(array, 0.0)
                return array


            r_channel=bilinear_interp(r_channel)
            g_channel=bilinear_interp(g_channel)
            b_channel=bilinear_interp(b_channel)
            rgb_img = np.zeros((r_channel.shape[0], r_channel.shape[1], 3))

            rgb_img[:,:,0]=r_channel
            rgb_img[:,:,1]=g_channel
            rgb_img[:,:,2]=b_channel

            return rgb_img

        dms=False
        if dms:
            img = demosaic(img, bayer_pattern)
            np.save("../demosaiced", img)

        img=np.load("../demosaiced.npy")

        img=white_balance_postmosaic(img, method=wb_method, rgb_weights=[r_scale, g_scale, b_scale], coordinates=coordinate)






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


        rgb2xyz = np.array([[0.4124564, 0.3575761, 0.1804375],
                            [0.2126729, 0.7151522, 0.0721750],
                            [0.0193339, 0.1191920, 0.9503041]])
        xyz2cam = np.array([6988,-1384,-714,-5631,13410,2447,-1485,2204,7318]).reshape(3, 3, order='C')/10000


        csc=True
        if csc:
            img=color_space_correction(img, xyz2cam,rgb2xyz)
            np.save("../colorcorrected", img)

        img=np.load("../colorcorrected.npy")


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
        img=brightness_adj(img, target_mean=0.55)

        skimage.io.imsave(f"../image_{wb_method}_{coordinate}.png", (img*255).astype('uint8'))
        skimage.io.imsave(f"../image_{wb_method}_{coordinate}.jpg", (img*255).astype('uint8'))
