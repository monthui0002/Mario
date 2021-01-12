import os

tile_size = 16
scale = 2
w, h = (16 * tile_size * scale, 14 * tile_size * scale)
FPS = 60
delta = 5  # use in collision checking
list_map = []
for f in os.listdir("./levels"):
    list_map.append(f)
