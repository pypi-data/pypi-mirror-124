from converterpy.converter.quantity_based_converter import QuantityBasedConverter


class SIBaseConverter(QuantityBasedConverter):
    """
        ref: https://en.wikipedia.org/wiki/International_System_of_Units
    """

    def __init__(self, name, units, base_unit, quantity):
        super(SIBaseConverter, self).__init__(name, units, base_unit, quantity)

    def _conversion_table(self):
        raise NotImplementedError()

    # -----

    def map_source_value(self, source_value):
        if isinstance(source_value, str):
            return float(source_value)

        return source_value
