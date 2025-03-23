import math
from Triangle import Triangle  
from pprint import pprint 

def generate_triangles_with_depth(latitude, longitude, side_length_miles, depth):
    """
    Generates a list of Triangle objects based on a starting point, side length, and depth.

    Args:
        latitude (float): Latitude of the starting point.
        longitude (float): Longitude of the starting point.
        side_length_miles (float): Side length of the equilateral triangles in miles.
        depth (int): Number of layers of triangles to generate.

    Returns:
        list: A list of Triangle objects.
    """

    target_depth = depth  # Store the target depth
    current_depth = 0  # Initialize the current depth
    triangles = []  # List to store Triangle objects
    triangle_name = 1  # Initialize triangle name
    leds = 0  # Initialize LED counter
    current_points = [[latitude, longitude]]  # Starting point
    next_points = []  # List to store points for the next layer

    miles_per_degree_longitude = 45.0
    miles_per_degree_latitude = 69.0

    longitude_diff = side_length_miles / miles_per_degree_longitude
    height_miles = (side_length_miles * math.sqrt(3)) / 2
    latitude_diff = height_miles / miles_per_degree_latitude

    def calculate_triangle_center(coords):
        """Calculates the center (centroid) of a triangle."""
        lat_sum = sum(coord[0] for coord in coords)
        long_sum = sum(coord[1] for coord in coords)
        return [lat_sum / 3, long_sum / 3]

    def generate_single_triangle(lat, long, direction):
        """Generates coordinates for a single triangle based on direction."""
        if direction == "nw":
            bottom_left_lat = lat
            bottom_left_long = long - longitude_diff
            top_lat = lat + latitude_diff
            top_long = long - (longitude_diff / 2)
            return [[bottom_left_lat, bottom_left_long], [lat, long], [top_lat, top_long]]
        elif direction == "n":
            top_left_lat = lat + latitude_diff
            top_left_long = long - (longitude_diff / 2)
            top_right_lat = lat + latitude_diff
            top_right_long = long + (longitude_diff / 2)
            return [[top_left_lat, top_left_long], [top_right_lat, top_right_long], [lat, long]]
        elif direction == "ne":
            bottom_right_lat = lat
            bottom_right_long = long + longitude_diff
            top_lat = lat + latitude_diff
            top_long = long + (longitude_diff / 2)
            return [[lat, long], [bottom_right_lat, bottom_right_long], [top_lat, top_long]]
        elif direction == "se":
            top_right_lat = lat
            top_right_long = long + longitude_diff
            bottom_lat = lat - latitude_diff
            bottom_long = long + (longitude_diff / 2)
            return [[lat, long], [top_right_lat, top_right_long], [bottom_lat, bottom_long]]
        elif direction == "s":
            bottom_left_lat = lat - latitude_diff
            bottom_left_long = long - (longitude_diff / 2)
            bottom_right_lat = lat - latitude_diff
            bottom_right_long = long + (longitude_diff / 2)
            return [[bottom_left_lat, bottom_left_long], [bottom_right_lat, bottom_right_long], [lat, long]]
        elif direction == "sw":
            top_left_lat = lat
            top_left_long = long - longitude_diff
            bottom_lat = lat - latitude_diff
            bottom_long = long - (longitude_diff / 2)
            return [[top_left_lat, top_left_long], [lat, long], [bottom_lat, bottom_long]]
        else:
            return None

    def create_triangle_if_unique(coords, center):
        """Creates a Triangle object if its center is unique (rounded comparison)."""
        center_exists = False
        rounded_center = [round(center[0], 6), round(center[1], 6)]

        for existing_triangle in triangles:
            existing_rounded_center = [round(existing_triangle.get_centre()[0], 6), round(existing_triangle.get_centre()[1], 6)]
            if existing_rounded_center == rounded_center:
                center_exists = True
                break

        if not center_exists:
            nonlocal triangle_name, leds
            triangle = Triangle(triangle_name, [leds + 1, leds + 2], coords, center)
            triangles.append(triangle)
            triangle_name += 1
            leds += 2

    while current_depth < target_depth:
        temp_points = [] #collect next points to avoid changing next_points during iteration.
        for current_point in current_points:
            lat, long = current_point

            # Generate and process each of the six triangles
            for direction in ["nw", "n", "ne", "se", "s", "sw"]:
                coords = generate_single_triangle(lat, long, direction)
                if coords:
                    center = calculate_triangle_center(coords)
                    create_triangle_if_unique(coords, center)
                    for coord in coords: #append all points from the triangle to the next point list.
                        if coord not in temp_points:
                            temp_points.append(coord)

        current_depth += 1
        current_points = temp_points
        next_points = [] #reset next points.

    return triangles

# Example usage
latitude = 51.709339
longitude = -2.028522 
side_length_miles = 1.0
depth = 5

triangles = generate_triangles_with_depth(latitude, longitude, side_length_miles, depth)
# count the number of triangles
print(f"Number of triangles generated: {len(triangles)}")



def extract_triangle_vertices(triangle_objects):
    """
    Extracts the vertex coordinates from a list of Triangle objects.

    Args:
        triangle_objects (list): A list of Triangle objects.

    Returns:
        list: A nested list containing the vertex coordinates of each triangle.
    """

    locations = []
    for triangle in triangle_objects:
        locations.append(triangle.get_coordinates())

    return locations

# Example Usage (assuming you have 'triangles' from generate_triangles_with_depth)
locations = extract_triangle_vertices(triangles)
pprint(locations) #pretty print the results.