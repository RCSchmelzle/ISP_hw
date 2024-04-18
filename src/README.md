# To run the code, modify the following parameters and run:

# Image path:
img_path='data/baby.tiff'

# White balance method:
#   'preset':   Use the camera scaling from the dcraw recon run
#   'gray':     Use the gray world assumption
#   'white':    Use the white world assumption
#   'manual':   Input a pixel coordinate that represents a white patch
# Note: putting multiple in the array will run each variation on the image
wb_methods=[] 

# For 'manual' white balance, input candidate coordinates for white patches
# Some predefined coordinates are as follows:
#   Window Glare             [190, 3279],    
#   Window Glare             [420, 3658],    
#   Baby Eye                 [1082, 2442],   
#   Baby Eyebrow             [937, 2559],
#   Baby Shirt White Part    [2214, 1360],   
#   Baby Eye Glint           [1035, 1833]   
# Putting multiple stores multiple candidate coordinates
candidate_coordinates=[[190, 3279], [420, 3658]]

# Index into which candidate coordinate you want to process
# selected_coordinates==-1 processes all candidate coordinates
#   and yields an image for each
selected_coordinates=-1 
