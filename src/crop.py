import argparse
from importlib.machinery import SourceFileLoader
from PIL import Image

parser = argparse.ArgumentParser(
    description="Crops an image to a given bounding box"
)

parser.add_argument(
    "input_image",
    type=str,
    help="Input image file"
)

parser.add_argument(
    "input_data",
    type=str,
    help="Input site data file"
)

args = parser.parse_args()

# The data file is a Python script that returns a dictionary with our information
# We can import it and call the config() function to get the dictionary
data_name = args.input_data.split("/")[-1].split(".")[0]
data = SourceFileLoader(data_name, args.input_data).load_module().config()

# Disable decompression bomb protection
Image.MAX_IMAGE_PIXELS = None

image = Image.open(args.input_image)
image_width, image_height = image.size

# Calculate the pixel coordinates of the bounding box from the lat/lng coordinates
start_x = int((data["final_lng_west"] - data["raw_lng_west"]) /
              (data["raw_lng_east"] - data["raw_lng_west"]) * image_width)

start_y = int((data["raw_lat_north"] - data["final_lat_north"]) /
              (data["raw_lat_north"] - data["raw_lat_south"]) * image_height)

end_x = int((data["final_lng_east"] - data["raw_lng_west"]) /
            (data["raw_lng_east"] - data["raw_lng_west"]) * image_width)

end_y = int((data["raw_lat_north"] - data["final_lat_south"]) /
            (data["raw_lat_north"] - data["raw_lat_south"]) * image_height)

# Add 1 pixel of padding for slope calculation
start_x -= 1
start_y -= 1
end_x += 1
end_y += 1

# Crop the image
cropped_image = image.crop((start_x, start_y, end_x, end_y))

# Save the cropped image
cropped_image.save(f"{data['name']}_cropped.tif")

print(f"Original image size: {image_width}, {image_height}")
print(
    f"Cropped image size: {end_x - start_x}, {end_y - start_y} (including 1 pixel of padding)"
)
print(f"Image file saved as {data['name']}_cropped.tif")
