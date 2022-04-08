import json

COUNT = [1, 2, 3]  # every 1
COLOR = ["red", "blue", "green"]  # every 3
SHAPE = ["squiggle", "diamond", "round"]  # every 9
SHADE = ["solid", "striped", "empty"]  # every 27

tmp = {"count": 1, "shape": "sh", "color": "co", "shading": "hd", "image": "X.png"}


def create(path: str):
    """
    create the jsons description files and save them in the given `path`

    :param path: json directory
    """
    counts = COUNT * 27
    colors = [item for sublist in ([c] * 3 for c in COLOR) for item in sublist] * 9
    shapes = [item for sublist in ([s] * 9 for s in SHAPE) for item in sublist] * 3
    shades = [item for sublist in ([s] * 27 for s in SHADE) for item in sublist]
    data = zip(counts, colors, shapes, shades)
    for i, t in enumerate(data):
        tmp["count"] = t[0]
        tmp["shape"] = t[1]
        tmp["color"] = t[2]
        tmp["shading"] = t[3]
        tmp["image"] = f"{i + 1}.png"
        with open(f"{path}/{i + 1}.json", 'w') as f:
            f.write(json.dumps(tmp).replace(', ', ',\n').replace('}', '\n}').replace('{', '{\n'))
