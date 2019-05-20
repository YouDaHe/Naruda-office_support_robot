import math
import png
import numpy
import matplotlib.pyplot as plt
from PIL import Image, ImageOps


def dist2d(point1, point2):
    """
    Euclidean distance between two points
    :param point1:
    :param point2:
    :return:
    """

    x1, y1 = point1[0:2]
    x2, y2 = point2[0:2]

    dist2 = (x1 - x2)**2 + (y1 - y2)**2

    return math.sqrt(dist2)


def png_to_ogm(filename, normalized=False, origin='lower'):
    """
    Convert a png image to occupancy data.
    :param filename: the image filename
    :param normalized: whether the data should be normalised, i.e. to be in value range [0, 1]
    :param origin:
    :return:
    """

    # additional edit: it inverses image. because it has opposite representation with SLAM driven map
    image = Image.open(filename)
    if image.mode == 'RGBA':
        r, g, b, a = image.split()
        rgb_image = Image.merge('RGB', (r, g, b))
        inverted_image = ImageOps.invert(rgb_image)
        r2, g2, b2 = inverted_image.split()
        final_transparent_image = Image.merge('RGBA', (r2, g2, b2, a))
        final_transparent_image.save('./inv_map.png')
    else:
        inverted_image = ImageOps.invert(image)
        inverted_image.save('./inv_map.png')

    r = png.Reader('./inv_map.png')
    img = r.read()
    img_data = list(img[2])

    out_img = []
    bitdepth = img[3]['bitdepth']

    for i in range(len(img_data)):

        out_img_row = []

        for j in range(len(img_data[0])):
            if j % img[3]['planes'] == 0:
                if normalized:
                    out_img_row.append(img_data[i][j]*1.0/(2**bitdepth))
                else:
                    out_img_row.append(img_data[i][j])

        out_img.append(out_img_row)

    if origin == 'lower':
        out_img.reverse()

    return out_img


def plot_path(path):
    start_x, start_y = path[0]
    goal_x, goal_y = path[-1]

    # plot path
    path_arr = numpy.array(path)
    plt.plot(path_arr[:, 0], path_arr[:, 1], 'y')

    # plot start point
    plt.plot(start_x, start_y, 'ro')

    # plot goal point
    plt.plot(goal_x, goal_y, 'go')

    plt.show()
