import math
from pprint import pprint

def generate_six_triangles(latitude, longitude):
    """
    Generates six equilateral triangles around a given coordinate.

    Args:
        latitude (float): Latitude of the central coordinate.
        longitude (float): Longitude of the central coordinate.

    Returns:
        list: A 2D list of triangle coordinates.
    """

    side_length_miles = 1.0
    miles_per_degree_longitude = 45.0
    miles_per_degree_latitude = 69.0

    longitude_diff = side_length_miles / miles_per_degree_longitude
    height_miles = (side_length_miles * math.sqrt(3)) / 2
    latitude_diff = height_miles / miles_per_degree_latitude

    triangles = []

    # 1. Northwest
    nw_bottom_left_lat = latitude
    nw_bottom_left_long = longitude - longitude_diff
    nw_top_lat = latitude + latitude_diff
    nw_top_long = longitude - (longitude_diff / 2)
    triangles.append([[nw_bottom_left_lat, nw_bottom_left_long], [latitude, longitude], [nw_top_lat, nw_top_long]])

    # 2. North
    n_top_left_lat = latitude + latitude_diff
    n_top_left_long = longitude - (longitude_diff / 2)
    n_top_right_lat = latitude + latitude_diff
    n_top_right_long = longitude + (longitude_diff / 2)
    triangles.append([[n_top_left_lat, n_top_left_long], [n_top_right_lat, n_top_right_long], [latitude, longitude]])

    # 3. Northeast
    ne_bottom_right_lat = latitude
    ne_bottom_right_long = longitude + longitude_diff
    ne_top_lat = latitude + latitude_diff
    ne_top_long = longitude + (longitude_diff / 2)
    triangles.append([[latitude, longitude], [ne_bottom_right_lat, ne_bottom_right_long], [ne_top_lat, ne_top_long]])

    # 4. Southeast
    se_top_right_lat = latitude
    se_top_right_long = longitude + longitude_diff
    se_bottom_lat = latitude - latitude_diff
    se_bottom_long = longitude + (longitude_diff / 2)
    triangles.append([[latitude, longitude], [se_top_right_lat, se_top_right_long], [se_bottom_lat, se_bottom_long]])

    # 5. South
    s_bottom_left_lat = latitude - latitude_diff
    s_bottom_left_long = longitude - (longitude_diff / 2)
    s_bottom_right_lat = latitude - latitude_diff
    s_bottom_right_long = longitude + (longitude_diff / 2)
    triangles.append([[s_bottom_left_lat, s_bottom_left_long], [s_bottom_right_lat, s_bottom_right_long], [latitude, longitude]])

    # 6. Southwest
    sw_top_left_lat = latitude
    sw_top_left_long = longitude - longitude_diff
    sw_bottom_lat = latitude - latitude_diff
    sw_bottom_long = longitude - (longitude_diff / 2)
    triangles.append([[sw_top_left_lat, sw_top_left_long], [latitude, longitude], [sw_bottom_lat, sw_bottom_long]])

    return triangles

# Example Usage:
latitude = 51.709339 
longitude = -2.006299777777778
six_triangles = generate_six_triangles(latitude, longitude)
pprint(six_triangles)