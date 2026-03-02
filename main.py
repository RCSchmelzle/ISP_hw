import json
import os
import sys

import skimage.io

from isp import isp_pipeline


def load_raw_image(path):
    """Load a raw image (NEF, TIFF, etc.) and return the Bayer mosaic as a numpy array."""
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.nef', '.cr2', '.arw', '.dng', '.raw'):
        import rawpy
        with rawpy.imread(path) as raw:
            img = raw.raw_image_visible.copy().astype('double')
        return img
    else:
        return skimage.io.imread(path, plugin='pil').astype('double')


def main(config_path='config.json'):
    with open(config_path) as f:
        cfg = json.load(f)

    img_path = cfg['img_path']
    output_dir = cfg.get('output_dir', 'data/Outputs')
    wb_methods = cfg.get('wb_methods', ['gray'])
    black = cfg.get('black', 0)
    white = cfg.get('white', 16383)
    r_scale = cfg.get('r_scale', 1.0)
    g_scale = cfg.get('g_scale', 1.0)
    b_scale = cfg.get('b_scale', 1.0)
    candidate_coordinates = cfg.get('manual_coordinates', [])
    selected_idx = cfg.get('selected_coordinate_index', -1)

    os.makedirs(output_dir, exist_ok=True)

    img = load_raw_image(img_path)
    print(f'Width: {img.shape[1]}')
    print(f'Height: {img.shape[0]}')
    print(f'Data type: {img.dtype}')

    for wb_method in wb_methods:
        if wb_method == 'manual':
            if selected_idx != -1:
                coords = [candidate_coordinates[selected_idx]]
            else:
                coords = candidate_coordinates
        else:
            coords = [None]

        for coordinate in coords:
            print(f'White balance using {wb_method}' +
                  (f' at {coordinate}' if coordinate else ''))
            isp_pipeline(img, wb_method,
                         r_scale=r_scale, g_scale=g_scale, b_scale=b_scale,
                         coordinate=coordinate, black=black, white=white,
                         output_dir=output_dir)


if __name__ == '__main__':
    config = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
    main(config)
