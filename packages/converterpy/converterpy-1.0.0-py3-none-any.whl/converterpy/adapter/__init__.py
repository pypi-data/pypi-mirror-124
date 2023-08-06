from converterpy.converter import Converter
from converterpy.exception import ConversionNotSupportedException, UnexpectedResultException


class ConverterTextAdapter(Converter):

    def __init__(self, converter):
        super(ConverterTextAdapter, self).__init__(converter.name)

        # -----

        self.realConverter = converter

    def __repr__(self):
        return '%s adapter' % self.realConverter.name

    def supported_conversions(self):
        # todo should convert units to text ?
        return self.realConverter.supported_conversions()

    def is_source_unit_supported(self, source_selector):
        source_unit = ConverterTextAdapter._find_unit_by_selector(source_selector, self.supported_conversions().keys())
        return super(ConverterTextAdapter, self).is_source_unit_supported(source_unit)

    def get_convertible_target_units(self, source_selector):
        source_unit = ConverterTextAdapter._find_unit_by_selector(source_selector, self.supported_conversions().keys())
        return super(ConverterTextAdapter, self).get_convertible_target_units(source_unit)

    def is_convertible(self, source_selector, target_selector):
        assert isinstance(source_selector, str)
        assert isinstance(target_selector, str)

        source_unit, target_unit = self._get_source_target_units(source_selector, target_selector)

        return (source_unit is not None) and (target_unit is not None)

    def convert(self, source_selector, source_value, target_selector):
        assert isinstance(source_selector, str)
        assert isinstance(target_selector, str)

        source_unit, target_unit = self._get_source_target_units(source_selector, target_selector)

        if (source_unit is None) or (target_unit is None):
            raise ConversionNotSupportedException(self, source_unit, target_unit)

        return self.realConverter.convert(source_unit, source_value, target_unit)

    # -----

    def _get_source_target_units(self, source_selector, target_selector):
        supported_conversions = self.supported_conversions()

        source_unit = ConverterTextAdapter._find_unit_by_selector(source_selector, supported_conversions.keys())
        if not source_unit:
            self.logger.debug("[%s] Source unit is not found with selector [%s]" % (self.name, source_selector))
            return None, None

        target_unit = ConverterTextAdapter._find_unit_by_selector(target_selector, supported_conversions[source_unit])

        if not target_unit:
            self.logger.debug("[%s] Target unit is not found with selector [%s]" % (self.name, target_selector))
            return None, None

        return source_unit, target_unit

    # -----

    @staticmethod
    def _find_unit_by_selector(selector, units):
        units = [unit for unit in units if selector in [unit.shortname(), unit.fullname()]]

        if len(units) > 1:
            raise UnexpectedResultException("More than one unit found for [%s], found: [%s]" % (selector, units))

        return units[0] if len(units) > 0 else None
