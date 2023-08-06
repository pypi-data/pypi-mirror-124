from converterpy.converter.quantity_based_converter import Quantity
from converterpy.unit.quantityunit import QuantityUnit
from converterpy.converter.si import SIBaseConverter


QUANTITY_SI_LENGTH = Quantity("LENGTH")

UNIT_SI_MILLIMETER = QuantityUnit('mm', 'millimeter', QUANTITY_SI_LENGTH)
UNIT_SI_CENTIMETER = QuantityUnit('cm', 'centimeter', QUANTITY_SI_LENGTH)
UNIT_SI_METER = QuantityUnit('m', 'meter', QUANTITY_SI_LENGTH)
UNIT_SI_KILOMETER = QuantityUnit('km', 'kilometer', QUANTITY_SI_LENGTH)

SI_LENGTH_UNITS = [
    UNIT_SI_MILLIMETER,
    UNIT_SI_CENTIMETER,
    UNIT_SI_METER,
    UNIT_SI_KILOMETER
]


class SILengthConverter(SIBaseConverter):

    def __init__(self):
        super(SILengthConverter, self).__init__('SI Length Converter', SI_LENGTH_UNITS, UNIT_SI_METER,
                                                QUANTITY_SI_LENGTH)

        self.conversion_table = {
            UNIT_SI_MILLIMETER: 10**-3,
            UNIT_SI_CENTIMETER: 10**-2,
            UNIT_SI_METER: 1,
            UNIT_SI_KILOMETER: 10**3,
        }

    def _conversion_table(self):
        return self.conversion_table
