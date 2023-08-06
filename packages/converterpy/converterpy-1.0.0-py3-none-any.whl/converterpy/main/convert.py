import logging
import pathlib
import json
import sys

from converterpy.adapter import ConverterTextAdapter
from converterpy.converter import Converter
from converterpy.cli import Cli

from converterpy.exception import SuitableConverterNotFoundException, MultipleSuitableConverterException
from converterpy.provider.builtin import BuiltinConverterProvider
from converterpy.util.assertion import assert_list_is_instance
from converterpy.util.logger import LogManager, LEVEL_OUT
from converterpy.util.import__ import import_class


class Config(object):

    @staticmethod
    def from_file(path='/etc/converterpy.json'):
        logger = LogManager.get_logger()

        configs = None
        if pathlib.Path(path).exists():
            logger.debug("reading config file [%s]" % path)
            with open(path) as fd:
                content = fd.read()
                configs = json.loads(content)
        else:
            logger.warning("Config file not found [%s], using defaults" % path)

        return Config(configs)

    # ------

    def __init__(self, configs=None, use_built_in_provider=True):
        if configs is None:
            configs = list()

        assert isinstance(configs, list)
        assert_list_is_instance(configs, dict)

        self.provider_configs = configs
        self.use_built_in_provider = use_built_in_provider


class ConvertMain(object):

    # ------

    @staticmethod
    def find_suitable_converters_to_convert(converters, source_selector, target_selector):
        assert_list_is_instance(converters, Converter)
        assert isinstance(source_selector, str)
        assert isinstance(target_selector, str)

        return [c for c in converters if c.is_convertible(source_selector, target_selector)]

    # ------

    def __init__(self, logger, config):
        self.config = config
        self.logger = logger

        self.converters = []
        self.init_providers(config.provider_configs)

        if config.use_built_in_provider:
            self.provide_converters(BuiltinConverterProvider())

    def init_providers(self, provider_configs):
        self.logger.debug("Found [%s] provider configs" % len(provider_configs))
        for cfg in provider_configs:
            clazz = import_class(**cfg)

            provider = clazz()
            self.provide_converters(provider)

    def provide_converters(self, provider):
        converters = provider.provide()

        assert_list_is_instance(converters, Converter)

        self.logger.debug("adding [%s] new converters [%s]" % (len(converters), converters))
        return self.add_converters(converters)

    def add_converters(self, converters):
        self.converters.extend([ConverterTextAdapter(converter) for converter in converters])

    def find_candidate_converters_to_convert(self, source_selector):
        assert isinstance(source_selector, str)

        return [c for c in self.converters if c.is_source_unit_supported(source_selector)]

    def find_converter(self, source_selector, target_selector):
        candidate_converters = self.find_candidate_converters_to_convert(source_selector)
        self.logger.debug("%s candidate converters found: %s" % (len(candidate_converters), candidate_converters))
        if len(candidate_converters) == 0:
            raise SuitableConverterNotFoundException("Suitable converter not found for for source [%s]"
                                                     % source_selector)

        suitable_converters = self.find_suitable_converters_to_convert(candidate_converters, source_selector,
                                                                       target_selector)
        self.logger.debug("%s suitable converters found: %s" % (len(suitable_converters), suitable_converters))
        if len(suitable_converters) == 0:
            convertible_targets = []
            for c in candidate_converters:
                convertible_targets.extend(c.get_convertible_target_units(source_selector))

            raise SuitableConverterNotFoundException("Suitable converter not found for for source [%s] and target [%s] "
                                                     "selectors" % (source_selector, target_selector),
                                                     convertible_targets)
        elif len(suitable_converters) > 1:
            raise MultipleSuitableConverterException("More than one converter found found for source [%s] and target "
                                                     "[%s] selectors, found: [%s]" % (source_selector, target_selector,
                                                                                      suitable_converters))

        return suitable_converters[0]

    def convert(self, source_selector, source_value, target_selector):
        try:
            converter = self.find_converter(source_selector, target_selector)
            self.logger.debug('Converter [%s] is selected for conversion [%s] to [%s]' %
                              (converter.name, source_selector, target_selector))
        except SuitableConverterNotFoundException as e:
            if e.convertible_target_unit:
                return "%s\n  Convertible units from [%s] are %s" % (e, source_selector, e.convertible_target_unit)
            else:
                return str(e)
        except MultipleSuitableConverterException as e:
            return str(e)

        return converter.convert(source_selector, source_value, target_selector)

    def list_conversions(self, source_selector=None):
        conversions = dict()
        for converter in self.converters:
            available_conversions = converter.supported_conversions()
            if source_selector and len(available_conversions) > 0:
                filtered_conversions = dict()
                for source, target in available_conversions.items():
                    if source_selector in (source.shortname(), source.fullname()):
                        filtered_conversions[source] = target

                available_conversions = filtered_conversions

            if len(available_conversions) > 0:
                conversions[converter.name] = available_conversions

        return conversions

    def run(self, cli):
        if cli.action == 'convert':
            source_value = cli.value
            source_selector = cli.source
            target_selector = cli.target
            return self.convert(source_selector, source_value, target_selector)
        elif cli.action == 'list':
            source_selector = cli.source
            conversions = self.list_conversions(source_selector)

            list_of_conversions = ""
            for converter_name, conversions in conversions.items():
                list_of_conversions += "[%s]\n" % converter_name
                for source, target in conversions.items():
                    list_of_conversions += "  [%s] -> %s\n" % (repr(source), target)

            return 'List of available conversions:\n\n%s' % list_of_conversions


def main():
    # be initializer of logger to set log_format
    logger_name = LogManager.DEFAULT_LOGGER_NAME
    logger = LogManager.create_logger(name=logger_name, level=LEVEL_OUT, log_format='%(message)s')

    cli = Cli(sys.argv[1:])

    # ------

    if cli.verbose:
        LogManager.override_format(logger_name, LogManager.DEFAULT_LOG_FORMAT)
        LogManager.override_log_level(logger_name, logging.DEBUG)

    logger.debug("Parsed args: %s" % cli.__dict__)

    # ------

    cfg = Config.from_file()
    convert_main = ConvertMain(logger, cfg)
    try:
        result_value = convert_main.run(cli)
        logger.out(result_value)
    except Exception as e:
        logger.out("Generic error occurred, see more with verbose options")
        logger.debug("Error: %s" % e)


if __name__ == "__main__":
    main()
