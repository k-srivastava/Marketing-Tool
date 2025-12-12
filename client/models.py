"""
Models for responses from the AI client.
"""
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


class FontRecommendation(BaseModel):
    """
    Represents font names and HTML links to load fonts into CSS>

    :ivar font_1: First font name.
    :type font_1: str
    :ivar font_1_link: HTML link tag for the first font.
    :ivar font_2: Second font name.
    :type font_2: str
    :ivar font_2_link: HTML link tag for the second font.
    :type font_2_link: str
    :ivar font_3: Third font name.
    :type font_3: str
    :ivar font_3_link: HTML link tag for the third font.
    :type font_3_link: str
    :ivar font_4: Fourth font name.
    :type font_4: str
    :ivar font_4_link: HTML link tag for the fourth font.
    :type font_4_link: str
    """
    font_1: str
    font_1_link: str
    font_2: str
    font_2_link: str
    font_3: str
    font_3_link: str
    font_4: str
    font_4_link: str


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
