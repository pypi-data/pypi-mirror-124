from typing import Optional

from MSApi.Attribute import Attribute
from MSApi.ObjectMS import check_init


class AttributeMixin:

    @check_init
    def gen_attributes(self):
        for attr in self._json.get('attributes', []):
            yield Attribute(attr)

    def get_attribute_by_name(self, name: str) -> Optional[Attribute]:
        for attr in self.gen_attributes():
            if attr.get_name() == name:
                return attr
        return None