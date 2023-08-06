import datetime
import re

from converterpy.converter import Converter
from converterpy.exception import ConversionNotSupportedException, SuitableDateFormatNotFoundException
from converterpy.unit import Unit

UNIT_TIMESTAMP = Unit('ts', 'timestamp')
UNIT_DATE = Unit('dt', 'date')


class TimestampDateConverter(Converter):

    DATE_FORMAT = f"%Y-%m-%d %H:%M:%S"

    def __init__(self, timezone=None):
        super(TimestampDateConverter, self).__init__('Timestamp Date converter')

        self.timezone = timezone
        self.regex_to_date_format = {
            "^[0-9]{4}-[0-9]{2}-[0-9]{2}$": f"%Y-%m-%d",
            "^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$": f"%Y-%m-%d %H:%M:%S"
        }

    def supported_conversions(self):
        return {
            UNIT_TIMESTAMP: [UNIT_DATE],
            UNIT_DATE: [UNIT_TIMESTAMP]
        }

    def convert(self, source_unit, source_value, target_unit):
        assert isinstance(source_unit, Unit)
        assert isinstance(target_unit, Unit)

        if not self.is_convertible(source_unit, target_unit):
            raise ConversionNotSupportedException(self, source_unit, target_unit)

        # -----

        if source_unit == UNIT_TIMESTAMP and target_unit == UNIT_DATE:
            return self.timestamp_to_date(source_value)
        elif source_unit == UNIT_DATE and target_unit == UNIT_TIMESTAMP:
            return self.date_to_timestamp(source_value)
        else:
            raise ConversionNotSupportedException(self, source_unit, target_unit)

    # -----

    def timestamp_to_date(self, timestamp):
        if isinstance(timestamp, str):
            timestamp = int(timestamp)

        date = datetime.datetime.fromtimestamp(timestamp, tz=self.timezone)
        return date.strftime(TimestampDateConverter.DATE_FORMAT)

    def date_to_timestamp(self, date_str):
        date_str = date_str.strip()

        date_format = self.__choose_date_format(date_str)

        date = datetime.datetime.strptime(date_str, date_format)
        date = date.replace(tzinfo=self.timezone)
        return date.timestamp()

    # ------

    def __choose_date_format(self, date_str):
        for regex in self.regex_to_date_format:
            if re.match(regex, date_str):
                date_format = self.regex_to_date_format[regex]
                self.logger.debug("regex [%s] is matched and date format [%s] is chosen" % (regex, date_format))
                return date_format

        raise SuitableDateFormatNotFoundException(date_str)