
import os
import logging
import pathlib

from sentinel.profile import ( 
    LauncherProfile, 
    IncorrectProfileFormat,
    load_extra_vars 
)
from sentinel.dispatcher import Dispatcher
from sentinel.commands.common import Command
from sentinel.services.service_account import import_service_tokens


logger = logging.getLogger(__name__)


class LaunchCommand(Command):
    '''
    Launch Command
    '''
    name = 'launch'
    help = 'Launch attack detector(-s)'

    def add(self):
        '''
        Add Launch command and arguments
        '''
        self._parser.add_argument('--profile', type=pathlib.Path, required=True,
                            help='Sentinel Profile')
        self._parser.add_argument('--import-service-tokens', action='store_true',
                            help = "Import service tokens before launch")
        self._parser.add_argument('--vars', type=str, action='append',
                            help = "Set additional variables as JSON, " + \
                                   "if filename prepend with @. Support YAML/JSON file")
        self._parser.add_argument('--env-vars', type=str,
                            help = "Set environment variables from JSON/YAML file")

        self._parser.set_defaults(handler=self.handle)

        return self._parser

    def handle(self, args):
        ''' 
        Handling Fetch command arguments
        ''' 
        super().handle(args)
        
        extra_vars = load_extra_vars(args.vars)

        # Update env var from file
        if args.env_vars is not None:
            for k,v in load_extra_vars([f'@{args.env_vars}',]).items():
                os.environ[k] = v

        if args.import_service_tokens:
            logger.info('Importing service account tokens')
            import_service_tokens()

        try:
            profile = LauncherProfile().parse(profile_path=args.profile,
                                              extra_vars=extra_vars)
            dispatcher = Dispatcher(profile = profile)
            dispatcher.run()
        except IncorrectProfileFormat as err:
            logger.error(err)

