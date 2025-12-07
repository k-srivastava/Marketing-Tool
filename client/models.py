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
