import numpy as np


def color_space_correction(img, xyz2cam, rgb2xyz):
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
