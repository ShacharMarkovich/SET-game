from Card import Card


def __check_count(c1: Card, c2: Card, c3: Card):
    if c1.count == c2.count and c1.count == c3.count:
        return True
    elif c1.count != c2.count and c1.count != c3.count and c2.count != c3.count:
        return True

    return False


def __check_shape(c1: Card, c2: Card, c3: Card):
    if c1.shape == c2.shape and c1.shape == c3.shape:
        return True
    elif c1.shape != c2.shape and c1.shape != c3.shape and c2.shape != c3.shape:
        return True

    return False


def __check_shading(c1: Card, c2: Card, c3: Card):
    if c1.shading == c2.shading and c1.shading == c3.shading:
        return True
    elif c1.shading != c2.shading and c1.shading != c3.shading and c2.shading != c3.shading:
        return True

    return False


def __check_color(c1: Card, c2: Card, c3: Card):
    if c1.color == c2.color and c1.color == c3.color:
        return True
    elif c1.color != c2.color and c1.color != c3.color and c2.color != c3.color:
        return True

    return False


def check_set(c1: Card, c2: Card, c3: Card):
    return __check_count(c1, c2, c3) and __check_shape(c1, c2, c3) and \
           __check_shading(c1, c2, c3) and __check_color(c1, c2, c3)
