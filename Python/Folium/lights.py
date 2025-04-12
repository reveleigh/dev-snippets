from machine import Pin
import utime
import random
from neopixel import Neopixel

numpix = 300
strip = Neopixel(numpix, 0, 22, "GRB")
strip.brightness(200)

# Light uf the whole thing white
for i in range(numpix):
    strip[i] = (255, 255, 255)
strip.show()

# Wait a bit
utime.sleep(5)

leds = [
    [148, 149],
    [170, 171],
    [168, 169],
    [150, 151],
    [128, 129],
    [130, 131], #End Inner hexagon
    [132, 133],
    [146, 147],
    [172, 173],
    [186, 187],
    [188, 189],
    [210, 211],
    [208, 209],
    [190, 191],
    [192, 193],
    [166, 167],
    [152, 153],
    [126,127],
    [112, 113],
    [110, 111],
    [88, 89],
    [90, 91],
    [108, 109],
    [106, 107],
    [104, 105],
    [134, 135],
    [144, 145],
    [174, 175],
    [184, 185],
    [214, 215],
    [212, 213],
    [226, 227],
    [228, 229],
    [250, 251],
    [248, 249],
    [230, 231],
    [232, 233],
    [206, 207],
    [204, 205],
    [194, 195],
    [164, 165],
    [154, 155],
    [124, 125],
    [114, 115],
    [84, 85],
    [86, 87],
    [72, 73],
    [70, 71],
    [48, 49],
    [50, 51],
    [68, 69],
    [66, 67],
    [92, 93],
    [94, 95],
    [96, 97],
    [102, 103],
    [136, 137],
    [142, 143],
    [176, 177],
    [182, 183],
    [216, 217],
    [222, 223],
    [224, 225],
    [254, 255],
    [252, 253],
    [264, 265],
    [266, 267],
    [282, 283],
    [280, 281],
    [268, 269],
    [270, 271],
    [246, 247],
    [244, 245],
    [234, 235],
    [236, 237],
    [202, 203],
    [196, 197],
    [162, 163],
    [156, 157],
    [122, 123],
    [116, 117],
    [82, 83],
    [76, 77],
    [74, 75],
    [44, 45],
    [46, 47],
    [34, 35],
    [32, 33],
    [16, 17],
    [18, 19],
    [30, 31],
    [28, 29],
    [52, 53],
    [54, 55],
    [64, 65],
    [62, 63],
    [60, 61],
    [98, 99],
    [100, 101],
    [138, 139],
    [140, 141],
    [178, 179],
    [180, 181],
    [218, 219],
    [220, 221],
    [258, 259],
    [256, 257],
    [260, 261],
    [262, 263],
    [286, 287],
    [284, 285],
    [288, 289],
    [290, 291],
    [298, 299],
    [296, 297],
    [292, 293],
    [294, 295],
    [278, 279],
    [276, 277],
    [272, 273],
    [274, 275],
    [242, 243],
    [240, 241],
    [238, 239],
    [200, 201],
    [198, 199],
    [160, 161],
    [158, 159],
    [120, 121],
    [118, 119],
    [80, 81],
    [78, 79],
    [40, 41],
    [42, 43],
    [38, 39],
    [36, 37],
    [12, 13],
    [14, 15],
    [10, 11],
    [8, 9],
    [0, 1],
    [2, 3],
    [6, 7],
    [4, 5],
    [20, 21],
    [22, 23],
    [26, 27],
    [24, 25],
    [56, 57],
    [58, 59],
]


# turn each hex_led on from beginnging to end
for led in leds:
    strip[led[0]] = (255, 0, 0)
    strip[led[1]] = (255, 0, 0)
    strip.show()
    utime.sleep(0.05)

for led in leds:
    strip[led[0]] = (255, 255, 255)
    strip[led[1]] = (255, 255, 255)
    strip.show()
    utime.sleep(0.05)

# turn each hex_led off from end to beginning
for led in reversed(leds):
    strip[led[0]] = (0, 0, 0)
    strip[led[1]] = (0, 0, 0)
    strip.show()
    utime.sleep(0.05)

# Turn on concentric rings of hex_leds
for i in range(6):
    strip[leds[i][0]] = (255, 0, 0)
    strip[leds[i][1]] = (255, 0, 0)
strip.show()
utime.sleep(0.25)

for i in range(6, 25):
    strip[leds[i][0]] = (255, 0, 0)
    strip[leds[i][1]] = (255, 0, 0)
strip.show()
utime.sleep(0.25)

for i in range(25, 55):
    strip[leds[i][0]] = (255, 0, 0)
    strip[leds[i][1]] = (255, 0, 0)
strip.show()
utime.sleep(0.25)

for i in range(55, 97):
    strip[leds[i][0]] = (255, 0, 0)
    strip[leds[i][1]] = (255, 0, 0)
strip.show()
utime.sleep(0.25)

for i in range(97, 150):
    strip[leds[i][0]] = (255, 0, 0)
    strip[leds[i][1]] = (255, 0, 0) 
strip.show()
utime.sleep(0.25)

# Create a copy of the leds list to work with
available_leds = list(leds)

while available_leds:
    # Pick a random index from the current list of available LEDs
    random_index = random.randint(0, len(available_leds) - 1)

    # Get the LED pair at the random index
    chosen_led_pair = available_leds.pop(random_index)

    for i in range(0, 256, 5):
        # Turn the chosen led back to white
        strip[chosen_led_pair[0]] = (255, i, i)
        strip[chosen_led_pair[1]] = (255, i, i)
        strip.show()
        utime.sleep(0.05) 

# sleep a bit
utime.sleep(5)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)


# Create a continuous rainbow effect loop
while True:
    for i in range(256):
        for j in range(numpix):
            strip[j] = wheel((j + i) & 255)
        strip.show()
        utime.sleep(0.01)


