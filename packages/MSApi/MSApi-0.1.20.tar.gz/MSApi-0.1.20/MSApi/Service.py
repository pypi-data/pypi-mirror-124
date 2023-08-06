from typing import Optional

from MSApi.Assortment import Assortment
from MSApi.ProductFolder import ProductFolder
from MSApi.mixin import AttributeMixin


class Service(Assortment, AttributeMixin):
    def __init__(self, json):
        super().__init__(json)

    def get_productfolder(self) -> Optional[ProductFolder]:
        """Группа Товара"""
        result = self._json.get('productFolder')
        if result is None:
            return None
        return ProductFolder(result)
