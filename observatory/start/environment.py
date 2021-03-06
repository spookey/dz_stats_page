from os import getenv, path

from observatory.lib.parse import parse_bool, parse_int

APP_NAME = 'observatory'
MDL_NAME = __name__.split('.')[0]

THIS_DIR = path.abspath(path.dirname(__file__))
BASE_DIR = path.abspath(path.dirname(THIS_DIR))
ROOT_DIR = path.abspath(path.dirname(BASE_DIR))

LOG_LVL = getenv('LOG_LVL', 'info')

MIGR_DIR = path.abspath(path.join(ROOT_DIR, 'migrate'))

DATABASE = getenv('DATABASE', 'sqlite://')
DATABASE_DEV = getenv(
    'DATABASE_DEV',
    'sqlite:///{}'.format(
        path.abspath(path.join(ROOT_DIR, 'database_dev.sqlite'))
    ),
)

SECRET_FILE = getenv('SECRET_FILE', 'secret.key')
SECRET_BASE = getenv('SECRET_BASE', ROOT_DIR)

BCRYPT_LOG_ROUNDS = parse_int(getenv('BCRYPT_LOG_ROUNDS', '13'), fallback=13)

CSRF_STRICT = parse_bool(getenv('CSRF_STRICT', 'true'), fallback=True)

BACKLOG_DAYS = parse_int(getenv('BACKLOG_DAYS', '14'), fallback=True)

SP_API_ENABLE = parse_bool(getenv('SP_API_ENABLE', 'true'), fallback=True)
SP_API_PREFIX = getenv('SP_API_PREFIX', 'space_api')
SP_API_REFRESH = parse_int(
    getenv('SP_API_REFRESH', f'{60 * 300}'), fallback=60 * 300
)


TITLE = getenv('TITLE', 'Observatory')
HTML_LANG = getenv('HTML_LANG', 'en')
FAVICON = getenv('FAVICON', 'logo.png')

FMT_STRFTIME = getenv('FMT_STRFTIME', '%d.%m.%Y %H:%M:%S UTC')
FMT_MOMENT_DEFAULT = getenv('FMT_MOMENT_DEFAULT', 'DD. MMM YYYY HH:mm:ss')
FMT_MOMENT_MSECOND = getenv('FMT_MOMENT_MSECOND', 'DD. MMM YYYY HH:mm:SS')
FMT_MOMENT_SECOND = getenv('FMT_MOMENT_SECOND', 'DD. MMM YYYY HH:mm:ss')
FMT_MOMENT_MINUTE = getenv('FMT_MOMENT_MINUTE', 'DD. MMM YYYY HH:mm:ss')
FMT_MOMENT_HOUR = getenv('FMT_MOMENT_HOUR', 'DD. MMM YYYY HH:mm')
FMT_MOMENT_DAY = getenv('FMT_MOMENT_DAY', 'DD. MMM YYYY HH:mm')
FMT_MOMENT_WEEK = getenv('FMT_MOMENT_WEEK', 'DD. MMM YYYY')
FMT_MOMENT_MONTH = getenv('FMT_MOMENT_MONTH', 'DD. MMM YYYY')
FMT_MOMENT_QUARTER = getenv('FMT_MOMENT_QUARTER', 'MMM YYYY')
FMT_MOMENT_YEAR = getenv('FMT_MOMENT_YEAR', 'MMM YYYY')

API_PLOT_REFRESH_MS = parse_int(
    getenv('API_PLOT_REFRESH_MS', f'{60 * 1000}'), fallback=60 * 1000
)


TAGLINES = [
    getenv('TAGLINE_01', 'Hey Peter, what\'s happening?'),
    getenv('TAGLINE_02', 'Someone set us up the bomb!'),
    getenv('TAGLINE_03', 'We get signal!'),
    getenv('TAGLINE_04', 'Terror as a business!'),
    getenv('TAGLINE_05', 'Looking at numbers!'),
    getenv('TAGLINE_06', 'Rage against the virtual machine.'),
]

ICON = {
    '__fallback': getenv('ICON___FALLBACK', 'fire'),
    'bool_right': getenv('ICON_BOOL_RIGHT', 'check'),
    'bool_wrong': getenv('ICON_BOOL_WRONG', 'close'),
    'glob_descr': getenv('ICON_GLOB_DESCR', 'more'),
    'glob_empty': getenv('ICON_GLOB_EMPTY', 'emotion-sad'),
    'glob_error': getenv('ICON_GLOB_ERROR', 'flashlight'),
    'graph_init': getenv('ICON_GRAPH_INIT', 'focus-3'),
    'graph_zoom': getenv('ICON_GRAPH_ZOOM', 'search-eye'),
    'obj_mapper': getenv('ICON_OBJ_MAPPER', 'guide'),
    'obj_prompt': getenv('ICON_OBJ_PROMPT', 'newspaper'),
    'obj_sensor': getenv('ICON_OBJ_SENSOR', 'radar'),
    'obj_sp_api': getenv('ICON_OBJ_SP_API', 'braces'),
    'ops_arr_dn': getenv('ICON_OPS_ARR_DN', 'arrow-down-s'),
    'ops_arr_up': getenv('ICON_OPS_ARR_UP', 'arrow-up-s'),
    'ops_change': getenv('ICON_OPS_CHANGE', 'pencil'),
    'ops_create': getenv('ICON_OPS_CREATE', 'add'),
    'ops_delete': getenv('ICON_OPS_DELETE', 'delete-bin'),
    'ops_submit': getenv('ICON_OPS_SUBMIT', 'check-double'),
    'user_basic': getenv('ICON_USER_BASIC', 'user'),
    'user_enter': getenv('ICON_USER_ENTER', 'login-box'),
    'user_leave': getenv('ICON_USER_LEAVE', 'logout-box-r'),
}

ERROR_CODES = (
    400,
    401,
    403,
    404,
    418,
    500,
    501,
    502,
    503,
    504,
)
