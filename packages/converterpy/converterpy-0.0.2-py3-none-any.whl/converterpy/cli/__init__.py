class Cli(object):

    def __init__(self, logger):
        self.logger = logger

    def usage(self):
        return """
usage: convert <value> <source> to <target> [optional arguments]
       convert list [source]                [optional arguments]

    optional arguments:
    -h, --help          show help message
    -v                  verbose mode
        """

    # convert 10 seconds to minutes
    def parse(self, params):
        orig_params = params
        params = list(params)
        self.logger.debug("args: [%s]" % params)

        args = dict()

        # parse options
        for param in orig_params:
            if param in ['-h', '--help']:
                args['action'] = 'help'
                params.remove(param)
            elif param in ['-v', '--verbose']:
                args['verbose'] = True
                params.remove(param)
            elif param.startswith('-'):
                raise SyntaxError("Unexpected optional argument [%s]" % param)

        # if action is help, should not be changed
        if len(params) == 0 or ('action' in args and args['action'] == 'help'):
            args['action'] = 'help'
        elif params[0] == 'list':
            args['action'] = 'list'
            args['source'] = params[1] if len(params) > 1 else None
        else:
            args['action'] = 'convert'
            args['value'] = params[0]
            args['source'] = params[1]

            if params[2] != 'to':
                raise SyntaxError("Token error! Expected value: [to], found: [%s]" % params[2])

            args['target'] = params[3]

            self.logger.debug("CLI source_selector:%s source_value:%s target_value:%s"
                              % (args['source'], args['value'], args['target']))

        # ------

        self.validate(args)

        # ------

        return args

    def validate(self, parsed_args):
        if 'help' == parsed_args['action']:
            return

        def _val(n):
            if n not in parsed_args:
                raise SyntaxError("Argument [%s] is missing" % n)

        if 'convert' == parsed_args['action']:
            _val('value')
            _val('source')
            _val('target')
