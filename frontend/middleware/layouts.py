"""
Utility functions for the layout preference page.
"""
from PIL import Image, ImageOps


def generate_page_labels(num_support_images: int) -> list[str]:
    """
    Generate page labels for the layout preference page based on the number of support images.

    :param num_support_images: Number of support images to include in the layout.
    :type num_support_images: int

    :return: List of page labels.
    :rtype: list[str]
    """
    page_labels = ['Hero Image Placement', 'Product Logo Placement']

    for i in range(num_support_images):
        page_labels.append(f'Support Image ({i + 1}) Placement')

    return page_labels


def generate_page_headings(num_support_images: int) -> list[str]:
    """
    Generate headings for the layout preference page based on the number of support images.

    :param num_support_images: Number of support images to include in the layout.
    :type num_support_images: int

    :return: List of page headings.
    :rtype: list[str]
    """
    page_headings = ['Hero Layout', 'Logo Layout']

    for i in range(num_support_images):
        page_headings.append(f'Support Image ({i + 1}) Layout')

    return page_headings


def create_option_thumbnails(
        asset: Image.Image, canvas_size: int = 200, canvas_color: str = '#E5E5E5', border_color: str = '#14213D'
) -> list[Image.Image]:
    """
    Generates a list of thumbnails for an image asset, each positioned differently on a canvas of specified size and
    color, with an optional border around each canvas. The nine thumbnails represent all possible alignments of the
    asset on the canvas: top-left, top-center, top-right, center-left, center, center-right, bottom-left,
    bottom-center, and bottom-right.

    :param asset: Image asset to be used for creating thumbnails.
    :type asset: Image.Image
    :param canvas_size: Size of the square canvas in pixels.
    :type canvas_size: int
    :param canvas_color: Background color of the canvas in a web-compatible color format.
    :type canvas_color: str
    :param border_color: Color of the border being added around each canvas in a web-compatible color format.
    :type border_color: str

    :return: List of thumbnail images containing the asset positioned on a canvas with the specified size and colors.
    :rtype: list[Image.Image]
    """
    positions = _get_relative_positions(asset.size, canvas_size)

    thumbnails: list[Image.Image] = []
    for position in positions:
        canvas = Image.new('RGBA', (canvas_size, canvas_size), canvas_color)
        canvas.paste(asset, position, asset)
        bordered_canvas = ImageOps.expand(canvas, border=1, fill=border_color)
        thumbnails.append(bordered_canvas)

    return thumbnails


def get_thumbnail_position_name(idx: int) -> str:
    """
    Get the corresponding position name for a thumbnail index.

    :param idx: Thumbnail index.
    :type idx: int

    :return: Position name.
    :rtype: str
    """
    if idx == 0:
        return 'Top Left'
    elif idx == 1:
        return 'Top Center'
    elif idx == 2:
        return 'Top Right'
    elif idx == 3:
        return 'Middle Left'
    elif idx == 4:
        return 'Middle Center'
    elif idx == 5:
        return 'Middle Right'
    elif idx == 6:
        return 'Bottom Left'
    elif idx == 7:
        return 'Bottom Center'
    else:
        return 'Bottom Right'


def _get_relative_positions(asset_size: tuple[int, int], canvas_size: int) -> list[tuple[int, int]]:
    """
    Get the relative positions of the asset on a canvas.

    :param asset_size: Size of the asset in pixels.
    :type asset_size: tuple[int, int]
    :param canvas_size: Size of the canvas in pixels.
    :type canvas_size: int

    :return: Positions of the asset on the canvas.
    :rtype: tuple[int, int]
    """
    asset_width, asset_height = asset_size

    return [
        (0, 0),
        ((canvas_size - asset_width) // 2, 0),
        (canvas_size - asset_width, 0),

        (0, (canvas_size - asset_height) // 2),
        ((canvas_size - asset_width) // 2, (canvas_size - asset_height) // 2),
        (canvas_size - asset_width, (canvas_size - asset_height) // 2),

        (0, canvas_size - asset_height),
        ((canvas_size - asset_width) // 2, canvas_size - asset_height),
        (canvas_size - asset_width, canvas_size - asset_height)
    ]
