from converterpy.util.logger import LogManager


class Converter(object):

    def __init__(self, name):
        self.name = name
        self.logger = LogManager.get_logger()

    def supported_conversions(self):
        raise NotImplementedError()

    def convert(self, source_unit, source_value, target_unit):
        raise NotImplementedError()

    # ----

    def is_source_unit_supported(self, source_unit):
        return source_unit in self.supported_conversions()

    def get_convertible_target_units(self, source_unit):
        return self.supported_conversions()[source_unit]

    def is_convertible(self, source_unit, target_unit):
        return source_unit in self.supported_conversions() and target_unit in self.supported_conversions()[source_unit]

    # ----

    def __repr__(self):
        return 'Converter{%s}' % self.name
