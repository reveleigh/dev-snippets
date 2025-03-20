import math
from Triangle import Triangle  

def generate_triangles_with_depth(latitude, longitude, side_length_miles, depth):
    """
    Generates an array of Triangle objects based on a given point and depth.

    Args:
        latitude (float): Latitude of the starting point.
        longitude (float): Longitude of the starting point.
        side_length_miles (float): Side length of the triangles in miles.
        depth (int): The number of layers of triangles to generate.

    Returns:
        list: A list of Triangle objects.
    """

    centres = []
    led_value = 0
    triangle_name = 0
    triangles = []

    miles_per_degree_longitude = 45.0
    miles_per_degree_latitude = 69.0

    longitude_diff = side_length_miles / miles_per_degree_longitude
    height_miles = (side_length_miles * math.sqrt(3)) / 2
    latitude_diff = height_miles / miles_per_degree_latitude

    def calculate_triangle_center(coords):
        """Calculates the center of a triangle given its coordinates."""
        lat_sum = sum(coord[0] for coord in coords)
        long_sum = sum(coord[1] for coord in coords)
        return [lat_sum / 3, long_sum / 3]

    def generate_six_triangles(lat, long):
        """Generates six equilateral triangles around a given coordinate."""
        six_triangles_coords = []

        # Northwest
        nw_bottom_left_lat = lat
        nw_bottom_left_long = long - longitude_diff
        nw_top_lat = lat + latitude_diff
        nw_top_long = long - (longitude_diff / 2)
        six_triangles_coords.append([[nw_bottom_left_lat, nw_bottom_left_long], [lat, long], [nw_top_lat, nw_top_long]])

        # North
        n_top_left_lat = lat + latitude_diff
        n_top_left_long = long - (longitude_diff / 2)
        n_top_right_lat = lat + latitude_diff
        n_top_right_long = long + (longitude_diff / 2)
        six_triangles_coords.append([[n_top_left_lat, n_top_left_long], [n_top_right_lat, n_top_right_long], [lat, long]])

        # Northeast
        ne_bottom_right_lat = lat
        ne_bottom_right_long = long + longitude_diff
        ne_top_lat = lat + latitude_diff
        ne_top_long = long + (longitude_diff / 2)
        six_triangles_coords.append([[lat, long], [ne_bottom_right_lat, ne_bottom_right_long], [ne_top_lat, ne_top_long]])

        # Southeast
        se_top_right_lat = lat
        se_top_right_long = long + longitude_diff
        se_bottom_lat = lat - latitude_diff
        se_bottom_long = long + (longitude_diff / 2)
        six_triangles_coords.append([[lat, long], [se_top_right_lat, se_top_right_long], [se_bottom_lat, se_bottom_long]])

        # South
        s_bottom_left_lat = lat - latitude_diff
        s_bottom_left_long = long - (longitude_diff / 2)
        s_bottom_right_lat = lat - latitude_diff
        s_bottom_right_long = long + (longitude_diff / 2)
        six_triangles_coords.append([[s_bottom_left_lat, s_bottom_left_long], [s_bottom_right_lat, s_bottom_right_long], [lat, long]])

        # Southwest
        sw_top_left_lat = lat
        sw_top_left_long = long - longitude_diff
        sw_bottom_lat = lat - latitude_diff
        sw_bottom_long = long - (longitude_diff / 2)
        six_triangles_coords.append([[sw_top_left_lat, sw_top_left_long], [lat, long], [sw_bottom_lat, sw_bottom_long]])

        return six_triangles_coords

    def process_triangles(lat, long):
        """Processes the six triangles generated from a given point."""
        six_triangles_coords = generate_six_triangles(lat, long)

        for coords in six_triangles_coords:
            center = calculate_triangle_center(coords)
            if center not in centres:
                triangle_name += 1
                led_value += 2
                triangle = Triangle(triangle_name, [led_value - 1, led_value], coords, center)
                triangles.append(triangle)
                centres.append(center)
        return triangle_name, led_value

    current_lats = [latitude]
    current_longs = [longitude]

    for _ in range(depth):
        next_lats = []
        next_longs = []
        for lat, long in zip(current_lats, current_longs):
            triangle_name, led_value = process_triangles(lat, long)
            six_triangles_coords = generate_six_triangles(lat, long)
            for coords in six_triangles_coords:
                center = calculate_triangle_center(coords)
                next_lats.append(center[0])
                next_longs.append(center[1])
        current_lats = list(set(next_lats))
        current_longs = list(set(next_longs))

    return triangles
#Call function and print results
triangles = generate_triangles_with_depth(51.709339, -2.028522, 1.0, 2)
for triangle in triangles:
    print(f"Triangle {triangle.get_name()}:")
    print(f"LEDs: {triangle.get_leds()}")
    print(f"Coordinates: {triangle.get_coordinates()}")
    print(f"Center: {triangle.get_centre()}")
    print()