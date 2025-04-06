from pprint import pprint
from Triangle import Triangle  

def generate_triangles_with_depth(latitude, longitude, side_length_miles, depth):
    target_depth = depth  # Store the target depth
    current_depth = 0  # Initialize the current depth
    triangles = []  # List to store Triangle objects
    triangle_name = 1  # Initialize triangle name
    leds = 0  # Initialize LED counter
    current_points = [[latitude, longitude]]  # Starting point
    next_points = []  # List to store points for the next layer

    def get_triangle_center(coords):
        """Calculates the center (centroid) of a triangle."""
        lat_sum = sum(coord[0] for coord in coords)
        long_sum = sum(coord[1] for coord in coords)
        return [lat_sum / 3, long_sum / 3]


    def calculate_new_latitude(original_latitude, distance_miles, direction="north"):
        miles_per_degree_latitude = 69.0
        delta_latitude = distance_miles / miles_per_degree_latitude
        if direction.lower() == "north":
            return original_latitude + delta_latitude
        elif direction.lower() == "south":
            return original_latitude - delta_latitude
        else:
            return None

    def calculate_new_longitude(original_longitude, distance_miles, direction="east"):
        miles_per_degree_longitude = 45.0
        delta_longitude = distance_miles / miles_per_degree_longitude
        if direction.lower() == "east":
            return original_longitude + delta_longitude
        elif direction.lower() == "west":
            return original_longitude - delta_longitude
        else:
            return None
    

    def caculate_hexagon(center_lat, center_lon, side):
        points = []
        #push passed in lat and lon to the list
        points.append([center_lat, center_lon])

        # calculate the 6 points of the hexagon
        #top point
        lat = calculate_new_latitude(center_lat, side, "north")
        lon = center_lon
        points.append([lat, lon])

        #top right point
        lat = calculate_new_latitude(center_lat, side * 0.5, "north")
        lon = calculate_new_longitude(center_lon, side * 0.866025, "east")
        points.append([lat, lon])

        #bottom right point
        lat = calculate_new_latitude(center_lat, side * 0.5, "south")
        lon = calculate_new_longitude(center_lon, side * 0.866025, "east")
        points.append([lat, lon])

        #bottom point
        lat = calculate_new_latitude(center_lat, side, "south")
        lon = center_lon
        points.append([lat, lon])

        #bottom left point
        lat = calculate_new_latitude(center_lat, side * 0.5, "south")
        lon = calculate_new_longitude(center_lon, side * 0.866025, "west")
        points.append([lat, lon])

        #top left point
        lat = calculate_new_latitude(center_lat, side * 0.5, "north")
        lon = calculate_new_longitude(center_lon, side * 0.866025, "west")
        points.append([lat, lon])

        #close the hexagon by adding the first point again
        points.append([center_lat, center_lon])
        return points

    def calculate_triangles(points):
        triangles = []
        # Triangle 1
        triangle = [ points[0], points[1], points[2] ]
        triangles.append(triangle)

        # Triangle 2
        triangle = [ points[0], points[2], points[3] ]
        triangles.append(triangle)

        # Triangle 3
        triangle = [ points[0], points[3], points[4] ]
        triangles.append(triangle)

        # Triangle 4
        triangle = [ points[0], points[4], points[5] ]
        triangles.append(triangle)

        # Triangle 5
        triangle = [ points[0], points[5], points[6] ]
        triangles.append(triangle)

        # Triangle 6
        triangle = [ points[0], points[6], points[1] ]
        triangles.append(triangle)
        return triangles
    
    while current_depth < target_depth:
        #Get loop through the current points and calculate the hexagon for each point
        for current_point in current_points:
            lat, long = current_point
            #Calculate the hexagon for each point and add it to the temp points list
            hexagon = caculate_hexagon(lat, long, side_length_miles)
            #Calculate the triangles for each hexagon and add it to the temp triangles list
            t = calculate_triangles(hexagon)
            # Calculate the center of each triangle and add it to the temp triangles list
            for triangle in t:
                #get center of the triangle
                center = get_triangle_center(triangle)
                #loop through triangles and check if the center is unique
                center_exists = False
                rounded_center = [round(center[0], 6), round(center[1], 6)]
                for i in triangles:
                    existing_rounded_center = [round(i.get_centre()[0], 6), round(i.get_centre()[1], 6)]
                    if existing_rounded_center == rounded_center:
                        center_exists = True
                        break
                if not center_exists:
                    #create a new triangle object and add it to the triangles list
                    triangle = Triangle(triangle_name, [leds + 1, leds + 2], triangle, center)
                    triangles.append(triangle)
                    triangle_name += 1
                    leds += 2
            # put the coors of the hexagon into the next points list
            for i in range (1,7):
                next_points.append(hexagon[i])
        current_depth += 1
        current_points = next_points
        next_points = []
    return triangles
  


# Example usage
triangles = generate_triangles_with_depth(51.717400, -1.967829, 4, 5)
#Ptetty print the coordinates of the triangles
triangles_co = []
for triangle in triangles:
    triangles_co.append(triangle.get_coordinates())

# count the number of triangles
print(f"Number of triangles generated: {len(triangles)}")
# Print the coordinates of the triangles to a file
with open("triangles.txt", "w") as f:
    for triangle in triangles_co:
        f.write(f"{triangle},\n")