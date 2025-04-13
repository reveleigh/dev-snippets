import folium

# Assuming 'triangles.txt' contains the list of triangle coordinates
# in the format: [[lat1, lon1], [lat2, lon2], [lat3, lon3]],
locations = []
try:
    with open("triangles.txt", "r") as f:
        for line in f:
            try:
                coords_str = line.strip().rstrip(',')
                coords = eval(coords_str)
                if isinstance(coords, list) and all(isinstance(coord, list) and len(coord) == 2 and all(isinstance(c, float) for c in coord) for coord in coords):
                    locations.append(coords)
            except (SyntaxError, TypeError):
                print(f"Warning: Skipping invalid line in triangles.txt: {line.strip()}")
except FileNotFoundError:
    print("Error: triangles.txt not found. Cannot draw polygons.")

# Dictionary to store triangle information (name, LEDs, centre) from triangles_info.txt
triangle_info = {}
try:
    with open("triangles_info.txt", "r") as f:
        print("Opened triangles_info.txt successfully")  # DEBUG: File open check
        for line in f:
            if line.strip():
                print(f"Processing line: {line.strip()}")  # DEBUG: Line content
                # Extract parts more carefully
                name_part_str = line.split(", LED Numbers: ")[0]
                leds_part_str = line.split(", Centre: ")[0].split(", LED Numbers: ")[1]
                centre_part_str = line.split(", Centre: ")[1].strip()

                try:
                    name = int(name_part_str.split(": ")[1])
                    # Safely evaluate the LED numbers list
                    leds = eval(leds_part_str)
                    # Safely evaluate the Centre coordinates list
                    centre = eval(centre_part_str)

                    triangle_info[name] = {"leds": leds, "centre": centre}
                    print(f"Added to triangle_info: {triangle_info[name]}")  # DEBUG: Dictionary entry
                except (ValueError, TypeError, SyntaxError) as e:
                    print(f"Warning: Skipping invalid line in triangles_info.txt: {line.strip()}, Error: {e}")
                
except FileNotFoundError:
    print("Error: triangles_info.txt not found. Cannot add labels.")

# Initial map centered around a relevant location (adjust if needed)
m = folium.Map(location=(50.76948625883613, -13.144881632576398), tiles="cartodb voyager", zoom_start=10)

# Draw the triangles
if locations:
    folium.Polygon(
        locations=locations,
        color="blue",
        weight=2,
        fill_color="red",
        fill_opacity=0.2,
        fill=True,
    ).add_to(m)

# Add labels to the center of each triangle
if triangle_info:
    print(f"triangle_info dictionary: {triangle_info}")  # DEBUG: Full dictionary
    for name, info in triangle_info.items():
        center = info['centre']
        leds = info['leds']
        label_text = f"Triangle number: {name}, LEDs: {leds}"
        folium.Marker(
            location=center,
            popup=folium.Popup(label_text, parse_html=True),
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(m)
else:
    print("No triangle information available to add labels.")

# Save the map to an HTML file
m.save('hex_at_sea_with_labels.html')

print("Map with triangles and labels saved to hex_at_sea_with_labels.html")