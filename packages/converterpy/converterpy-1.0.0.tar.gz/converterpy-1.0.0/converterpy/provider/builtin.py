from converterpy.provider import ConverterProvider

from converterpy.converter.si.time_converter import SITimeConverter
from converterpy.converter.si.length_converter import SILengthConverter
from converterpy.converter.si.mass_converter import SIMassConverter
from converterpy.converter.timestamp_date_converter import TimestampDateConverter


class BuiltinConverterProvider(ConverterProvider):

    def provide(self):
        return [
            SITimeConverter(),
            SILengthConverter(),
            SIMassConverter(),
            TimestampDateConverter(),
        ]
