"""
End-to-end test of the ISP pipeline using a synthetic Bayer raw image.

Downloads a regular image, converts it into a simulated Bayer mosaic
(as if it came straight off a sensor), then runs the full ISP pipeline
to reconstruct a color image. The output should resemble the original.
"""
import os
import urllib.request

import numpy as np
import skimage.io

from isp import (
    linearize_image, bayer_id, wb_pre_demosaic, demosaic,
    color_space_correction, brightness_adj
)


def rgb_to_bayer(rgb_img, pattern='grbg'):
    """Convert an RGB image to a simulated Bayer mosaic (single-channel).

    This reverses demosaicing: for each pixel, keep only the color channel
    that the Bayer filter would pass through.
    """
    h, w, _ = rgb_img.shape
    bayer = np.zeros((h, w), dtype=rgb_img.dtype)

    # Channel indices: R=0, G=1, B=2
    pattern_map = {
        'grbg': {(0,0): 1, (0,1): 0, (1,0): 2, (1,1): 1},
        'gbrg': {(0,0): 1, (0,1): 2, (1,0): 0, (1,1): 1},
        'rggb': {(0,0): 0, (0,1): 1, (1,0): 1, (1,1): 2},
        'bggr': {(0,0): 2, (0,1): 1, (1,0): 1, (1,1): 0},
    }
    pmap = pattern_map[pattern]

    for (dy, dx), ch in pmap.items():
        bayer[dy::2, dx::2] = rgb_img[dy::2, dx::2, ch]

    return bayer


def generate_test_image(h=480, w=640):
    """Generate a synthetic test image with color gradients, shapes, and edges.

    Creates a reproducible test scene with known color regions so we can
    visually verify each ISP stage.
    """
    img = np.zeros((h, w, 3), dtype=np.uint8)

    # Sky gradient (top third)
    for y in range(h // 3):
        t = y / (h // 3)
        img[y, :] = [int(135 + 50*t), int(206 - 30*t), 235]

    # Green ground (bottom third)
    for y in range(2*h//3, h):
        t = (y - 2*h//3) / (h // 3)
        img[y, :] = [int(34 + 20*t), int(139 - 40*t), int(34 + 10*t)]

    # Brown middle band
    img[h//3:2*h//3, :] = [139, 90, 43]

    # Red rectangle
    img[h//4:h//4+80, w//6:w//6+120] = [220, 40, 40]

    # Blue rectangle
    img[h//2:h//2+80, w//2:w//2+120] = [40, 40, 220]

    # White patch (for white balance reference)
    img[50:90, w-140:w-40] = [240, 240, 240]

    # Yellow circle
    cy, cx, r = h//2 + 40, w//4, 50
    yy, xx = np.ogrid[:h, :w]
    mask = ((yy - cy)**2 + (xx - cx)**2) <= r**2
    img[mask] = [230, 210, 40]

    # Gradient bar at bottom
    for x in range(w):
        t = x / w
        img[-30:, x] = [int(255*t), int(255*(1-t)), int(128)]

    return img


def main():
    output_dir = os.path.join(os.path.dirname(__file__), 'data', 'test_outputs')
    os.makedirs(output_dir, exist_ok=True)

    # Generate synthetic test image with known colors
    img = generate_test_image()
    print(f"Source image: {img.shape}, dtype={img.dtype}")

    # Make dimensions even for Bayer pattern
    h, w = img.shape[:2]
    img = img[:h - h % 2, :w - w % 2]

    # Save the original for comparison
    skimage.io.imsave(os.path.join(output_dir, 'original.jpg'), img, quality=95)

    # Simulate a 14-bit Bayer raw sensor image (GRBG pattern)
    pattern = 'grbg'
    img_float = img.astype('double') / 255.0
    bayer_raw = rgb_to_bayer(img_float, pattern)

    # Scale to 14-bit range [0, 16383] like a real sensor
    bayer_14bit = (bayer_raw * 16383).astype('double')

    print(f"Synthetic Bayer raw: {bayer_14bit.shape}, range=[{bayer_14bit.min():.0f}, {bayer_14bit.max():.0f}]")

    # --- Run each pipeline stage ---

    # 1. Linearize
    linear = linearize_image(bayer_14bit.copy(), black=0, white=16383)
    print(f"1. Linearize: range=[{linear.min():.3f}, {linear.max():.3f}]")

    # 2. Bayer ID
    detected = bayer_id(linear)
    print(f"2. Bayer ID: detected={detected} (expected={pattern})")

    # 3. White balance (gray world)
    wb = wb_pre_demosaic(linear.copy(), detected, method='gray')
    print(f"3. White balance (gray): range=[{wb.min():.3f}, {wb.max():.3f}]")

    # 4. Demosaic
    rgb = demosaic(wb.copy(), detected)
    print(f"4. Demosaic: shape={rgb.shape}, range=[{rgb.min():.3f}, {rgb.max():.3f}]")

    # 5. Color space correction
    rgb2xyz = np.array([[0.4124564, 0.3575761, 0.1804375],
                        [0.2126729, 0.7151522, 0.0721750],
                        [0.0193339, 0.1191920, 0.9503041]])
    xyz2cam = np.array([6988,-1384,-714,-5631,13410,2447,-1485,2204,7318]).reshape(3, 3, order='C')/10000

    corrected = color_space_correction(rgb.copy(), xyz2cam, rgb2xyz)
    print(f"5. Color correction: range=[{corrected.min():.3f}, {corrected.max():.3f}]")

    # 6. Brightness + gamma
    final = brightness_adj(corrected.copy(), target_mean=0.55)
    final = np.clip(final, 0, 1)
    print(f"6. Brightness/gamma: range=[{final.min():.3f}, {final.max():.3f}]")

    # Save result
    out_path = os.path.join(output_dir, 'pipeline_output.png')
    skimage.io.imsave(out_path, (final * 255).astype('uint8'))
    print(f"\nPipeline output saved to: {out_path}")
    print("Compare with original at: " + os.path.join(output_dir, 'original.jpg'))
    print("\nAll pipeline stages completed successfully!")


if __name__ == '__main__':
    main()
