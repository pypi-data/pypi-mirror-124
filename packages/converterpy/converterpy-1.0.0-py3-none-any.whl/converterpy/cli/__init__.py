from docopt import docopt
from converterpy.version import VERSION

# -----

USAGE = """
Usage:
  convert <value> <source> to <target> [-v|--verbose]
  convert <source> to <target> <value> [-v|--verbose]
  convert list [<source>] [-v|--verbose]
  convert --version

Options:
  -h --help        Show usage.
  -v --verbose     Enable verbose mode for debugging.
  --version        Show version.
"""

# -----


class Cli(object):

    def __init__(self, argv, usage=USAGE):
        assert isinstance(argv, list)

        self._usage = usage

        self.verbose = False
        self.source = None
        self.target = None
        self.value = None
        self.action = None
        self.version = VERSION

        # ----

        self.__parse(argv)

    def usage(self):
        return self._usage

    def __parse(self, argv):
        if len(argv) == 0:
            argv += ["--help"]
        args = docopt(self.usage(), argv=argv, version=self.version)

        # ---

        action = 'help'
        if args.get("list"):
            action = "list"
        elif args.get("to") and args.get("<source>") and args.get("<target>"):
            action = 'convert'

        self.action = action

        # ----

        self.verbose = args.get('--verbose')
        self.source = args.get('<source>')
        self.target = args.get('<target>')
        self.value = args.get('<value>')
