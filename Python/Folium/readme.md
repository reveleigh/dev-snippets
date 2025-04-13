# Folium experiments

I am beginning to experiment with Folium, a Python library that allows you to create interactive maps. This is a simple example of how to lay triangles over a map.

## Installation

You'll first need to install the Folium library. You can do this by running the following command:

```bash
pip install folium
```

## Generate a map with hexagons and triangles

I am working on an LED display project that requires an geographical area to be broken into triangles (I'll put a full write up elsewhere at some point).

To achieve this `hex_map_creator.py` takes user input for centre point of the map, the number of hexagons to be displayed, and the size of the hexagons. It then generates a map with hexagons and triangles overlaid on top. A dated "HexMap" folder is created which contains the HTML file along with a json file containing the coordinates of the triangles - along with other bits I'll need elsewhere.

Here in Gloucestershire, UK, one degree of longitude is approximately 45 miles. If you are using this elsewhere in the world you may need to adjust this value.

## Example hex map generations

If flat sides are selected:
!()[flat_sides.png](flat_sides.png)

If flat tops are selected:
!()[flat_top.png](flat_top.png)
