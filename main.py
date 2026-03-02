import os

import skimage.io

from isp import isp_pipeline

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

output_dir = os.path.join(os.path.dirname(__file__), 'data', 'Outputs')
os.makedirs(output_dir, exist_ok=True)

# Run all different variants
for wb_method in wb_methods:
    if wb_method=='manual':
        manual_coordinates=candidate_coordinates
        if selected_coordinates!=-1:
            manual_coordinates=[candidate_coordinates[selected_coordinates]]
    else:
        manual_coordinates=[None]

    for coordinate in manual_coordinates:
        isp_pipeline(img, wb_method, r_scale=r_scale, g_scale=g_scale, b_scale=b_scale,
                     coordinate=coordinate, black=black, white=white, output_dir=output_dir)
