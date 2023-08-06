from converterpy.converter import Converter
from converterpy.unit.quantityunit import QuantityUnit

from converterpy.util.assertion import assert_list_is_instance
from converterpy.exception import ConversionNotSupportedException


class Quantity(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Quantity(%s)' % self.name


class QuantityBasedConverter(Converter):

    @staticmethod
    def create_supported_conversion_dictionary(units):
        supported_conversions = dict()
        for unit in units:
            supported_conversions[unit] = [u for u in units]

        return supported_conversions

    # ------

    def __init__(self, name, units, base_unit, quantity):
        super(QuantityBasedConverter, self).__init__(name)

        assert isinstance(quantity, Quantity)
        assert isinstance(base_unit, QuantityUnit)
        assert_list_is_instance(units, QuantityUnit)

        # ---

        self.units = units  # list
        self.base_unit = base_unit
        self._quantity = quantity

        self._validate_init_args()

        self._supported_conversions = QuantityBasedConverter.create_supported_conversion_dictionary(self.units)

        # ----

    def _validate_init_args(self):
        if self.base_unit not in self.units:
            raise Exception("Base unit [%s] is not in units [%s]" % (self.base_unit, self.units))

        for unit in self.units:
            if unit.quantity() != self.quantity():
                raise Exception("Unit's quantity [%s] is not same with converter's quantity [%s]"
                                % (unit.quantity, self.quantity()))

    def _conversion_table(self):
        raise NotImplementedError()

    def map_source_value(self, source_value):
        return source_value

    # -----

    def quantity(self):
        return self._quantity

    # -----

    def supported_conversions(self):
        return self._supported_conversions

    def convert(self, source_unit, source_value, target_unit):
        assert isinstance(source_unit, QuantityUnit)
        assert isinstance(target_unit, QuantityUnit)

        if not self.is_convertible(source_unit, target_unit):
            raise ConversionNotSupportedException(self, source_unit, target_unit)

        if not (self.quantity() == source_unit.quantity() == target_unit.quantity()):
            raise Exception("Source unit's [%s] or target unit's [%s] quantity are not matched with [%s]"
                            % (source_unit.fullname(), target_unit.fullname(), self.quantity()))

        # -----

        source_value = self.map_source_value(source_value)

        conversion_table = self._conversion_table()
        base_unit_value = conversion_table[source_unit] * source_value

        return base_unit_value / conversion_table[target_unit]
