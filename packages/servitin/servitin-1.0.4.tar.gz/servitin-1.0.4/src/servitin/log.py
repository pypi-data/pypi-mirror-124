import logging
import logging.config
import time

from django.conf import settings


class Log:
    def __init__(self, logger, app_name):
        self.logger = logger
        self.app_name = app_name

    def info(self, msg, id=None, name=None):
        log(self.logger, 'info', self.app_name, msg, id_str=id, subsys_name=name)

    def critical(self, msg, tb=None, id=None, name=None):
        log(self.logger, 'critical', self.app_name, msg, id_str=id, traceback=tb, subsys_name=name)

    def error(self, msg, id=None, tb=None, name=None):
        log(self.logger, 'error', self.app_name, msg, id_str=id, traceback=tb, subsys_name=name)


def configure_logging(services):
    """
    Initialize main and logstash loggers
    :param settings: Kirservice settings
    """

    # add servitin formatter
    settings.LOGGING['formatters'].update(settings.SERVITIN_LOGGING['formatters'])

    for s in services:
        app_log_settings = getattr(settings, f"SERVITIN_{s['app_name'].upper()}_LOGGING", None)

        if app_log_settings:
            for x in settings.LOGGING.items():
                if x[0] == 'formatters':
                    x[1].update(app_log_settings.get('formatters', {}))
                if x[0] == 'handlers':
                    x[1].update(app_log_settings.get('handlers', {}))
                if x[0] == 'loggers':
                    x[1].update(app_log_settings.get('loggers', {}))

        logging.config.dictConfig(settings.LOGGING)
        logging.Formatter.converter = time.gmtime

        # init service logger
        logger = logging.getLogger(f"servitin_{s['app_name']}_logger")
        s['logger'] = logger
        s['log'] = Log(logger, s["app_name"])


def log(logger, level, service_name, msg, subsys_name=None, id_str=None, traceback=None, additional=None):
    """
    Logs message with main and logstash loggers
    :param logger: Logger instance
    :param level: Logger level
    :param service_name: Service name. exmpl: Kirservice or Collector
    :param msg: Message string
    :param subsys_name: Subsys name. exmpl: SocketServer or Postgres
    :param id_str: Entry id string
    :param traceback: Formatted traceback info
    :param additional: Additional info
    """
    prefix = f'[{service_name}]' if not subsys_name else f'[{service_name}] [{subsys_name}]'
    prefix = prefix if not id_str else f'{prefix} [{id_str}]'
    msg_str = f'{prefix} {msg}' if not traceback else f'{prefix} {msg}\n{traceback}'
    getattr(logger, level)(msg_str)

