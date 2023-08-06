from MSApi.ObjectMS import ObjectMS, check_init, SubObjectMS
from MSApi.PriceType import PriceType


class SalePrice(SubObjectMS):
    def __init__(self, json):
        super().__init__(json)

    def get_value(self) -> float:
        return self._json.get('value')/100

    def get_price_type(self) -> PriceType:
        return PriceType(self._json.get('priceType'))


class Assortment(ObjectMS):

    def __init__(self, json):
        super().__init__(json)

    @check_init
    def get_id(self) -> str:
        return self._json.get('id')

    @check_init
    def get_name(self) -> str:
        return self._json.get('name')

    @check_init
    def gen_sale_prices(self):
        """Цены продажи."""
        json_sale_prices = self._json.get('salePrices')
        if json_sale_prices is None:
            return
        for json_sale_price in json_sale_prices:
            yield SalePrice(json_sale_price)
