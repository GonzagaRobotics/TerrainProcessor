import argparse
import numpy as np
from PIL import Image

parser = argparse.ArgumentParser(
    description="Calculates the navmesh from the terrain data"
)

parser.add_argument(
    "input_image",
    type=str,
    help="Input image file"
)

parser.add_argument(
    "max_slope_angle",
    type=float,
    help="Approximate slope angle beyond which the cell is considered impassable"
)

args = parser.parse_args()

# Disable decompression bomb protection
Image.MAX_IMAGE_PIXELS = None

# Import image and convert to numpy array
img = Image.open(args.input_image)
data = np.array(img, np.float32)
img_width, img_height = img.size

# Free the image from memory
img.close()

# Calculate the slope of the terrain

# Initialize a 3D array to store the slope of the terrain
slope = np.zeros((img_height - 2, img_width - 2, 2), np.float32)

# 0 (Red) - North/South slope
slope[:, :, 0] = np.abs(data[:-2, 1:-1] - data[2:, 1:-1])

# 1 (Green) - East/West slope
slope[:, :, 1] = np.abs(data[1:-1, :-2] - data[1:-1, 2:])

# The resolution of the terrain data is about 1m/pixel
max_slope = np.tan(args.max_slope_angle * np.pi / 180)

# Mark the cells with a slope greater than the maximum slope angle as impassable
for i in range(2):
    slope[:, :, i] = np.where(slope[:, :, i] > max_slope, 1, 0)

# Pack the slope data into a single channel
final = np.zeros((img_height - 2, img_width - 2), np.uint8)

# First bit - North/South slope
final |= slope[:, :, 0].astype(np.uint8)

# Second bit - East/West slope
final |= slope[:, :, 1].astype(np.uint8) << 1

# Determine the output file name based on the input file name (ex. URC_cropped.tif -> URC_slope.png)
output_name = args.input_image.split("/")[-1]
output_name = output_name.split(".")[0]
output_name = output_name.split("_")[0] + "_slope.png"

Image.fromarray(final, mode="L").save(output_name, optimize=True)
