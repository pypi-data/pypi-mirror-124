# converterpy

converterpy is designed as a customizable conversion tool to convert one thing to another.

# Usage

```bash
usage: convert <value> <source> to <target> [optional arguments]

    optional arguments:
    -h, --help          show help message
    -v                  verbose mode
```

#### Examples

```bash
$ convert 3600 seconds to minutes -> '60'
$ convert 3600 sec to min -> '60'
$ convert 2500 g to kg -> '2.5'
$ convert 1610744400 ts to date -> '2021-01-16 00:00:00'
$ convert 100 centimeter to meter -> '1'
```

# Features
There are some built-in converters to use;
- SITimeConverter (converts the following units: seconds, minutes, hours)
- SILengthConverter (converts the following units: millimeter, centimeter, meter, kilometer)
- SIMassConverter (converts the following units: milligram, gram, kilogram)
- TimestampDateConverter (converts unix timestamp to date, date to timestamp format)

### Installation

```converterpy``` requires Python 3.5+ to run.

Install with pip

```sh
$ pip install converterpy
```

### Custom Converters

Please follow the instructions in custom converter [documentation.][custom_converter.doc]


License
----

MIT

[custom_converter.doc]: <https://github.com/bilalekremharmansa/converterpy/blob/main/docs/custom_converters.md>