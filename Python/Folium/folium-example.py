import folium
m = folium.Map(location=(51.709339, -2.028522), tiles="cartodb voyager", zoom_start=15)

locations = [
    [
        [51.709339, -2.028522], 
        [51.709339, -2.006299777777778], 
        [51.72189009280847, -2.017410888888889],
        ], 
    [
        [51.709339, -2.006299777777778], 
        [51.709339, -2.028522], 
        [51.69678790719153, -2.017410888888889]
    ], 
]


folium.Polygon(
    locations=locations,
    color="blue",
    weight=2,
    fill_color="red",
    fill_opacity=0.2,
    fill=True,
).add_to(m)

m.save('folium.html')