import argparse
from geopy.distance import geodesic
import geopy

parser = argparse.ArgumentParser(
    description='Calculates bounding box for a given GPS coordinate and radius'
)

parser.add_argument(
    "lat",
    type=float,
    help="Latitude of the center point in decimal degrees"
)
parser.add_argument(
    "lng",
    type=float,
    help="Longitude of the center point in decimal degrees"
)
parser.add_argument("radius", type=float, help="Radius in meters")

args = parser.parse_args()


def main():
    origin = geopy.Point(args.lat, args.lng)
    radius = args.radius

    # Calculate the north, east, south, and west points
    north = geodesic(meters=radius).destination(origin, 0).latitude
    east = geodesic(meters=radius).destination(origin, 90).longitude
    south = geodesic(meters=radius).destination(origin, 180).latitude
    west = geodesic(meters=radius).destination(origin, 270).longitude

    print(
        f"From {origin.format_decimal()} with radius {radius}m, the bounding box is:"
    )
    print(f"North: {north} degrees latitude")
    print(f"East: {east} degrees longitude")
    print(f"South: {south} degrees latitude")
    print(f"West: {west} degrees longitude")


if __name__ == "__main__":
    main()
