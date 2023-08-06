from converterpy.converter.quantity_based_converter import Quantity
from converterpy.unit.quantityunit import QuantityUnit
from converterpy.converter.si import SIBaseConverter


QUANTITY_SI_MASS = Quantity("MASS")

UNIT_SI_MILLIGRAM = QuantityUnit('mg', 'milligram', QUANTITY_SI_MASS)
UNIT_SI_GRAM = QuantityUnit('g', 'gram', QUANTITY_SI_MASS)
UNIT_SI_KILOGRAM = QuantityUnit('kg', 'kilometer', QUANTITY_SI_MASS)

SI_MASS_UNITS = [
    UNIT_SI_MILLIGRAM,
    UNIT_SI_GRAM,
    UNIT_SI_KILOGRAM
]


class SIMassConverter(SIBaseConverter):

    def __init__(self):
        super(SIMassConverter, self).__init__('SI Mass Converter', SI_MASS_UNITS, UNIT_SI_GRAM, QUANTITY_SI_MASS)

        self.conversion_table = {
            UNIT_SI_MILLIGRAM: 10**-3,
            UNIT_SI_GRAM: 1,
            UNIT_SI_KILOGRAM: 10**3,
        }

    def _conversion_table(self):
        return self.conversion_table
