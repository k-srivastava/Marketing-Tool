"""
Utility functions for the layout preference page.
"""


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
