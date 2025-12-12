"""
Models for responses from the AI client.
"""
from typing import Tuple

from pydantic import BaseModel


class ProductInformation(BaseModel):
    """
    Represents detailed information about a product.

    This class is used to store and manage product details, such as the name, tagline, brand, and a list of features
    associated with the product.

    :ivar name: The name of the product.
    :type name: str
    :ivar tagline: The tagline associated with the product.
    :type tagline: str
    :ivar brand_name: The name of the brand the product belongs to.
    :type brand_name: str
    :ivar features: A list of features describing the product.
    :type features: list[str]
    """
    name: str
    tagline: str
    brand_name: str
    features: list[str]


class ColorCurator(BaseModel):
    """
    Represents color curation recommendation for the product.
    This class is used to store and manage color curation recommendations.
    :ivar color_scheme_1 : colour schemes in a tuple consisting of primary and secondary colour hex codes in strings
    :type color_scheme_1: Tuple[str, str]
    :ivar color_scheme_2 : colour schemes in a tuple consisting of primary and secondary colour hex codes in strings
    :type color_scheme_2: Tuple[str, str]
    :ivar color_scheme_3 : colour schemes in a tuple consisting of primary and secondary colour hex codes in strings
    :type color_scheme_3: Tuple[str, str]
    :ivar color_scheme_4 : colour schemes in a tuple consisting of primary and secondary colour hex codes in strings
    :type color_scheme_4: Tuple[str, str]



    """
    color_scheme_1: Tuple[str, str]
    color_scheme_2: Tuple[str, str]
    color_scheme_3: Tuple[str, str]
    color_scheme_4: Tuple[str, str]
