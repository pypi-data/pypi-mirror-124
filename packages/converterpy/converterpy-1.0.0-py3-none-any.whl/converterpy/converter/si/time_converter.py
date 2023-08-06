from converterpy.converter.quantity_based_converter import Quantity
from converterpy.unit.quantityunit import QuantityUnit
from converterpy.converter.si import SIBaseConverter


QUANTITY_SI_TIME = Quantity("TIME")

UNIT_SI_SECOND = QuantityUnit('s', 'seconds', QUANTITY_SI_TIME)
UNIT_SI_MINUTE = QuantityUnit('m', 'minutes', QUANTITY_SI_TIME)
UNIT_SI_HOUR = QuantityUnit('h', 'hour', QUANTITY_SI_TIME)

SI_TIME_UNITS = [
    UNIT_SI_SECOND,
    UNIT_SI_MINUTE,
    UNIT_SI_HOUR
]


class SITimeConverter(SIBaseConverter):

    def __init__(self):
        super(SITimeConverter, self).__init__('SI Time Converter', SI_TIME_UNITS, UNIT_SI_SECOND, QUANTITY_SI_TIME)

        self.conversion_table = {
            UNIT_SI_SECOND: 1,
            UNIT_SI_MINUTE: 1*60,
            UNIT_SI_HOUR: 1*60*60,
        }

    def _conversion_table(self):
        return self.conversion_table
