import numpy as np
import skimage.io

from .linearize import linearize_image
from .bayer import bayer_id
from .white_balance import wb_pre_demosaic, wb_post_demosaic
from .demosaic import demosaic
from .color_correction import color_space_correction
from .tone_mapping import brightness_adj


# Full Pipeline
def isp_pipeline(img, wb_method, r_scale=1.0, g_scale=1.0, b_scale=1.0, coordinate=None,
                 black=0, white=16383, output_dir="."):
    img=linearize_image(img, black=black, white=white)
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

    skimage.io.imsave(f"{output_dir}/image_{wb_method}_{coordinate}.png", (img*255).astype('uint8'))
    skimage.io.imsave(f"{output_dir}/image_{wb_method}_{coordinate}_95.jpg", (img*255).astype('uint8'), quality=95)
