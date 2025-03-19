import math

def get_triangle(latitude, longitude, direction="up"):
    """
    Calculates the coordinates of an equilateral triangle with a 1-mile side length.

    Args:
        latitude (float): Latitude of the bottom-left vertex.
        longitude (float): Longitude of the bottom-left vertex.
        direction (str): "up" or "down", indicating the triangle's orientation.

    Returns:
        list: A list of three coordinate pairs (latitude, longitude) representing the vertices.
    """

    side_length_miles = 1.0
    miles_per_degree_longitude = 45.0
    miles_per_degree_latitude = 69.0

    longitude_diff = side_length_miles / miles_per_degree_longitude
    height_miles = (side_length_miles * math.sqrt(3)) / 2
    latitude_diff = height_miles / miles_per_degree_latitude

    if direction.lower() == "up":
        bottom_right_latitude = latitude
        bottom_right_longitude = longitude + longitude_diff

        top_latitude = latitude + latitude_diff
        top_longitude = longitude + (longitude_diff / 2)

        return [[latitude, longitude], [bottom_right_latitude, bottom_right_longitude], [top_latitude, top_longitude]]

    elif direction.lower() == "down":
        bottom_right_latitude = latitude
        bottom_right_longitude = longitude - longitude_diff

        top_latitude = latitude - latitude_diff
        top_longitude = longitude - (longitude_diff / 2)

        return [[latitude, longitude], [bottom_right_latitude, bottom_right_longitude], [top_latitude, top_longitude]]

    else:
        return "Invalid direction. Please use 'up' or 'down'."

# Example usage 1:  up
latitude = 51.709339 
longitude = -2.006299777777778
example_up = get_triangle(latitude, longitude, "down")
print(f"Cirencester Triangle (Up): {example_up}")

