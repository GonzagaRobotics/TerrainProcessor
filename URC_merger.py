from PIL import Image
import numpy as np


tr_lat_north = 38.48811896800004
tr_lng_east = -110.65601321399998
tr_lat_south = 38.397717801000056
tr_lng_west = -110.77095939499998

br_lat_north = 38.39799751000004
br_lng_east = -110.65644067999995
br_lat_south = 38.30759584900005
br_lng_west = -110.77124310699998

bl_lat_north = 38.39816533800007
bl_lng_east = -110.77095939499998
bl_lat_south = 38.30787466100003
bl_lng_west = -110.88562123699995

tl_lat_north = 38.48828733500005
tl_lng_east = -110.77067441199995
tl_lat_south = 38.39799751000004
tl_lng_west = -110.88547938


def overlap_old_new(name):
    old = Image.open(f"URC_{name}_2018.tif")
    new = Image.open(f"URC_{name}_2020.tif")

    # Create a mask from the new image
    mask = np.array(new, np.float32)
    mask = np.where(mask > 0, 255, 0).astype(np.uint8)
    mask = Image.fromarray(mask)

    # Overlap the new image on top of the old image
    old.paste(new, None, mask)

    # Free the new image from memory
    new.close()

    return old


tr = overlap_old_new("TR")
br = overlap_old_new("BR")
bl = overlap_old_new("BL")
tl = overlap_old_new("TL")

# Create a new image with the four images, one in each corner
full_width = tr.width + br.width
full_height = tr.height + bl.height

# We also need to adjust them, since they overlap each other by a small amount
tr_tl_lng_overlap = tr_lng_west - tl_lng_west
