import os
import sys
import time
import json
import traceback
import logging
from subprocess import check_call
from ._base import BaseCommand
from ...config import ConfigParserC  # pylint: disable=import-error


logger = logging.getLogger('vstutils')

UWSGI_EXTRA_ARGS = [
    'listen',
    'disable-logging',
    'log-4xx',
    'log-5xx',
]


class Command(BaseCommand):
    interactive = True
    help = "Run uwsgi server with configuration from ENV."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            'args',
            metavar='uwsgi_arg=value', nargs='*',
            help='Args "name=value" uwsgi server.',
        )
        parser.add_argument(
            '--migrate-attempts', '-a',
            default=60,
            dest='attempts', help='The number of attempts to migrate.',
        )

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.prefix = self._settings('VST_PROJECT_LIB', 'vstutils').upper()
        project_name = self._settings('VST_PROJECT', 'vstutils')

        logger.debug(f'Prefix={self.prefix} | Project={project_name}')

        config = self.prepare_config()
        env = dict()
        env[self._settings('CONFIG_ENV_DATA_NAME')] = config.generate_config_string()
        default_envs = {
            'UWSGI_PROCESSES': 'UWSGI_WORKERS',
            'UWSGI_THREADS': 'UWSGI_THREADS'
        }
        for key in default_envs:
            value = os.environ.get(f"{self.prefix}_{key}", '')
            if value:
                env[default_envs[key]] = value  # nocv

        if config['main']['debug'] or self._settings('TESTS_RUN', False):
            logger.debug(f'Env:\n{json.dumps(env, indent=4)}')
            logger.debug(f'Config:\n{env[self._settings("CONFIG_ENV_DATA_NAME")]}')

        success = False
        error = 'Unknown error.'
        for i in range(options.get('attempts', 60)):
            try:
                check_call(
                    [sys.executable, '-m', project_name, 'migrate'],
                    env=env, bufsize=0, universal_newlines=True,
                )
            except:
                error = traceback.format_exc()
                self._print(f"Retry #{i}...", 'WARNING')
                time.sleep(1)
            else:
                success = True
                break
        if success:
            try:
                check_call(
                    [sys.executable, '-m', project_name, self._settings('WEBSERVER_COMMAND', 'web')],
                    env=env, bufsize=0, universal_newlines=True,
                )
            except KeyboardInterrupt:  # nocv
                self._print('Exit by user...', 'WARNING')
                return
        else:
            self._print(error, 'ERROR')
            sys.exit(10)

    def prepare_config(self):
        # pylint: disable=too-many-locals,too-many-branches,too-many-statements
        prefix = self.prefix
        # SQLite prepearing
        sqlite_default_dir = os.environ.get(f'{prefix}_SQLITE_DIR', '/')
        if sqlite_default_dir != '/' and not os.path.exists(sqlite_default_dir):  # nocv
            os.makedirs(sqlite_default_dir)
        if sqlite_default_dir[-1] != '/':  # nocv
            sqlite_default_dir += '/'
        sqlite_default_name = os.environ.get(f'{prefix}_SQLITE_DBNAME', 'db.sqlite3')
        sqlite_db_path = f'{sqlite_default_dir}/{sqlite_default_name}'

        # Start configuring config file
        self.config = ConfigParserC()
        config = self.config

        # Set log level
        log_level = os.getenv(f'{prefix}_LOG_LEVEL', 'WARNING')
        # Set default settings
        config['main'] = {
            'debug': os.getenv(f'{prefix}_DEBUG', 'false'),
            'log_level': log_level,
            'timezone': os.getenv(f'{prefix}_TIMEZONE', 'UTC'),
            'enable_admin_panel': os.getenv(f'{prefix}_ENABLE_ADMIN_PANEL', 'false'),
            'first_day_of_week': os.getenv(
                f'{prefix}_FIRST_DAY_OF_WEEK',
                self._settings('FIRST_DAY_OF_WEEK')
            )
        }
        # ldap-server, ldap-default-domain if exist
        ldap_server = os.getenv(f'{prefix}_LDAP_CONNECTION', None)
        if ldap_server:  # nocv
            config['main']['ldap_server'] = ldap_server
        ldap_default_domain = os.getenv(f'{prefix}_LDAP_DOMAIN', None)
        if ldap_default_domain:  # nocv
            config['main']['ldap-default-domain'] = ldap_default_domain

        # Set db config
        if os.getenv(f'{prefix}_DB_HOST') is not None:
            try:
                pm_type = os.getenv(f'{prefix}_DB_TYPE', 'mysql')

                default_port = ''
                if pm_type == 'mysql':
                    default_port = '3306'
                elif pm_type == 'postgresql':  # nocv
                    default_port = '5432'

                config['database'] = {
                    'engine': f'django.db.backends.{pm_type}',
                    'name': os.environ[f'{prefix}_DB_NAME'],
                    'user': os.environ[f'{prefix}_DB_USER'],
                    'password': os.environ[f'{prefix}_DB_PASSWORD'],
                    'host': os.environ[f'{prefix}_DB_HOST'],
                    'port': os.getenv(f'{prefix}_DB_PORT', default_port),
                }
                config['database.options'] = {
                    'connect_timeout': os.getenv(f'{prefix}_DB_CONNECT_TIMEOUT', '20'),
                }
                if pm_type == 'mysql':
                    config['database.options']['init_command'] = os.getenv('DB_INIT_CMD', '')
            except KeyError:  # nocv
                raise Exception('Not enough variables for connect to  SQL server.')
        else:  # nocv
            config['database'] = {
                'engine': 'django.db.backends.sqlite3',
                'name': sqlite_db_path
            }

        # Set cache and locks config
        cache_loc = os.getenv('CACHE_LOCATION', f'/tmp/{prefix}_django_cache')
        cache_type = os.getenv(f'{prefix}_CACHE_TYPE', 'file')
        if cache_type == 'file':
            cache_engine = 'django.core.cache.backends.filebased.FileBasedCache'
        elif cache_type == 'memcache':  # nocv
            cache_engine = 'django.core.cache.backends.memcached.MemcachedCache'
        elif cache_type == 'redis':  # nocv
            cache_engine = 'django_redis.cache.RedisCache'
        else:  # nocv
            raise Exception(f'Unknown cache type `{cache_type}`.')

        config['cache'] = config['locks'] = {
            'backend': cache_engine,
            'location': cache_loc
        }

        # Set rpc settings
        rpc_connection = os.getenv('RPC_ENGINE', None)
        config['rpc'] = {
            'heartbeat': os.getenv('RPC_HEARTBEAT', '5'),
            'concurrency': os.getenv('RPC_CONCURRENCY', '4'),
            'clone_retry_count': os.getenv('RPC_CLONE_RETRY_COUNT', '3')
        }
        if rpc_connection:  # nocv
            config['rpc']['connection'] = rpc_connection

        # Set web server and API settings
        config['web'] = {
            'session_timeout': os.getenv(f'{prefix}_SESSION_TIMEOUT', '2w'),
            'rest_page_limit': os.getenv(f'{prefix}_WEB_REST_PAGE_LIMIT', '100'),
            'enable_gravatar': os.getenv(f'{prefix}_WEB_GRAVATAR', 'true'),
            'request_max_size': os.getenv(
                f'{prefix}_REQUEST_MAX_SIZE',
                self._settings('DATA_UPLOAD_MAX_MEMORY_SIZE')
            ),
            'x_frame_options': os.getenv(
                f'{prefix}_X_FRAME_OPTIONS',
                self._settings('X_FRAME_OPTIONS')
            ),
            'use_x_forwarded_host': os.getenv(
                f'{prefix}_USE_X_FORWARDED_HOST',
                self._settings('USE_X_FORWARDED_HOST')
            ),
            'use_x_forwarded_port': os.getenv(
                f'{prefix}_USE_X_FORWARDED_PORT',
                self._settings('USE_X_FORWARDED_PORT')
            ),
            'password_reset_timeout_days': os.getenv(
                f'{prefix}_PASSWORD_RESET_TIMEOUT_DAYS',
                self._settings('PASSWORD_RESET_TIMEOUT_DAYS')
            ),
            'secure_browser_xss_filter': os.getenv(
                f'{prefix}_SECURE_BROWSER_XSS_FILTER',
                self._settings('SECURE_BROWSER_XSS_FILTER')
            ),
            'secure_content_type_nosniff': os.getenv(
                f'{prefix}_SECURE_CONTENT_TYPE_NOSNIFF',
                self._settings('SECURE_CONTENT_TYPE_NOSNIFF')
            ),
            'secure_hsts_include_subdomains': os.getenv(
                f'{prefix}_SECURE_HSTS_INCLUDE_SUBDOMAINS',
                self._settings('SECURE_HSTS_INCLUDE_SUBDOMAINS')
            ),
            'secure_hsts_preload': os.getenv(
                f'{prefix}_SECURE_HSTS_PRELOAD',
                self._settings('SECURE_HSTS_PRELOAD')
            ),
            'secure_hsts_seconds': os.getenv(
                f'{prefix}_SECURE_HSTS_SECONDS',
                self._settings('SECURE_HSTS_SECONDS')
            ),
            'health_throttle_rate': os.getenv(
                f'{prefix}_HEALTH_THROTTLE_RATE',
                self._settings('HEALTH_THROTTLE_RATE').replace('/minute', '')
            ),
        }

        config['uwsgi'] = {
            'thread-stacksize': os.getenv(f'{prefix}_UWSGI_THREADSTACK', '40960'),
            'max-requests': os.getenv(f'{prefix}_UWSGI_MAXREQUESTS', '50000'),
            'limit-as': os.getenv(f'{prefix}_UWSGI_LIMITS', '512'),
            'harakiri': os.getenv(f'{prefix}_UWSGI_HARAKIRI', '120'),
            'vacuum': os.getenv(f'{prefix}_UWSGI_VACUUM', 'true'),
            'pidfile': os.getenv(f'{prefix}_UWSGI_PIDFILE', '/run/web.pid'),
            'daemon': 'false'
        }
        for uwsgi_param in UWSGI_EXTRA_ARGS:
            uwsgi_param_value = os.getenv(f'{prefix}_UWSGI_{uwsgi_param.upper()}', '')
            if uwsgi_param_value != '':
                config['uwsgi'][uwsgi_param] = uwsgi_param_value

        # Set worker settings
        config['rpc']['enable_worker'] = 'false'
        if os.environ.get('WORKER', '') == 'ENABLE':  # nocv
            config['rpc']['enable_worker'] = 'true'
            config['worker'] = {
                'loglevel': log_level,
                'logfile': f'/tmp/{prefix.lower()}_worker.log',
                'pidfile': f'/tmp/{prefix.lower()}_worker.pid',
                'beat': os.getenv(f'{prefix}_SCHEDULER_ENABLE', 'true')
            }

        mail_parameters = ['port', 'user', 'password', 'tls', 'ssl', 'from_address']
        mail_settings = dict(host=os.environ.get(f'{prefix}_MAIL_HOST'))
        if mail_settings['host']:
            for param in mail_parameters:
                value = os.environ.get(f'{prefix}_MAIL_{param.upper()}')
                if value:
                    mail_settings[param] = value
            config['mail'] = mail_settings

        # Set secret key
        os.environ.setdefault('SECRET_KEY', 'DISABLE')
        if os.environ['SECRET_KEY'] != 'DISABLE':  # nocv
            with open(f'/etc/{prefix.lower()}/secret', 'w') as secretfile:
                secretfile.write(os.environ['SECRET_KEY'])

        return config
