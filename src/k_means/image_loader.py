import os
from PIL import Image

import gendata


def load_image(image_name, output_file_name):
    """
    Safe image as RGB array to data directory
    :param str image_name: name of image in data folder
    :return int, int: loaded image size
    """
    # TODO fix this path
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    print(file_dir)
    file_name = image_name
    file_path = os.path.join(file_dir, 'data/' + file_name)

    with Image.open(file_path, 'r') as image:
        width, height = image.size
        pixel_values = list(image.getdata())
        gendata.save_to_file(pixel_values, output_file_name)
        return width, height
