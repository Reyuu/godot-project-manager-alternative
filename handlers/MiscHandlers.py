def get_contrasting_color(color):
    color = color[1:]
    color = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
    d = 0
    luminance = (0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]) / 255
    if luminance > 0.5:
        d = 0
    else:
        d = 255
    return "#{0:02x}{1:02x}{2:02x}".format(d, d, d)
