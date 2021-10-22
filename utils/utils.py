def get_max_height_width(lst):
    max_height = 0
    max_width = 0
    for x1, y1, x2, y2 in lst:
        height = y2 - y1
        width = x2 - x1
        max_height = max(max_height, height)
        max_width = max(max_width, width)

    return max_height, max_width
