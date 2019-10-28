import os
from PIL import Image

import gen_data


def load_image(image_name, output_file_name):
    """
    Save image as RGB array to data directory
    :param str image_name: name of image in data folder
    :param str output_file_name: output file name
    :return int, int: loaded image size
    """
    file_dir = os.path.dirname(os.path.realpath('__file__'))

    file_path = os.path.join(os.path.join(file_dir, 'data'), image_name)

    with Image.open(file_path, 'r') as image:
        width, height = image.size
        pixel_values = list(image.getdata())
        gen_data.save_to_file(pixel_values, output_file_name)

        return width, height
