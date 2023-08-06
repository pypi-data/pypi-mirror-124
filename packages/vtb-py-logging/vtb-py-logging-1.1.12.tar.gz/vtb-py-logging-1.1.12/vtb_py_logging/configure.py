import os
import sys
import logging
import pathlib
import functools
from vtb_py_logging import log_extra, DefaultColoredFormatter, SQLExtraFilter
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from vtb_py_logging import JsonFormatter
from distutils.util import strtobool


@functools.lru_cache()
def root_dir(stack_level=2):
    import inspect

    filename = None
    for frame in inspect.stack(0)[stack_level:]:
        if "site-packages" not in frame.filename:
            filename = frame.filename
            break

    # try to find .git folder
    if filename:
        parents = pathlib.Path(filename).parents
        for parent in parents:
            for path in parent.iterdir():
                if (path.is_dir() and path.name in (".git", ".idea", "venv")) or \
                   path.name in ("requirements.txt", ):
                    return parent

    bin_path = pathlib.Path(sys.argv[0]).parent
    return bin_path


def _get_file_handler(filename, rotate_mb, rotate_when, backup_count, log_level, file_suffix, change_suffix):
    filename = filename.with_suffix(file_suffix) if change_suffix else filename
    if rotate_mb:
        handler = RotatingFileHandler(filename, maxBytes=rotate_mb * 1024 * 1024, backupCount=backup_count,
                                      encoding="utf-8")

    elif rotate_when:
        handler = TimedRotatingFileHandler(filename, when=rotate_when, backupCount=backup_count, encoding="utf-8")
    else:
        handler = logging.FileHandler(filename, encoding="utf-8")

    handler.setLevel(log_level)
    return handler


def _init_handlers(logger, handler_names, filename, format_str, rotate_mb, rotate_when, backup_count, log_level,
                   json_multiline, log_colored):
    change_suffix = False
    for handler_name in handler_names:
        if handler_name == "simple":
            handler = _get_file_handler(filename, rotate_mb, rotate_when, backup_count, log_level,
                                        ".txt", change_suffix)
            formatter = logging.Formatter(format_str)
            handler.setFormatter(formatter)
            change_suffix = True
        elif handler_name == "json":
            handler = _get_file_handler(filename, rotate_mb, rotate_when, backup_count, log_level,
                                        ".json", change_suffix)
            formatter = JsonFormatter(multi_line=json_multiline)
            handler.setFormatter(formatter)
            change_suffix = True
        elif handler_name == "stderr":
            handler = logging.StreamHandler()
            formatter = DefaultColoredFormatter(format_str) if log_colored else logging.Formatter(format_str)
            handler.setFormatter(formatter)
        else:
            raise ValueError(f"unknown handler type: '{handler_name}'")

        logger.addHandler(handler)


_initialized = False


def _normalize_name(name):
    if name == "console":
        return "stderr"
    return name


def initialize_logging(app_name, filename=None, format_str=None, level=None, rotate_mb=None,
                       rotate_when=None, backup_count=7, json_multiline=False, cleanup=False):
    global _initialized
    if _initialized:
        return
    _initialized = True

    root = logging.root

    if cleanup:
        for h in root.handlers[:]:
            root.removeHandler(h)
            h.close()

    log_level = os.environ.get("LOG_LEVEL", level or "INFO")
    log_dir = os.environ.get("LOG_DIR")
    log_colored = strtobool(os.environ.get("LOG_COLORED", "true"))  # only for stderr
    log_sql = strtobool(os.environ.get("LOG_SQL", "false"))
    default_logger_level = os.environ.get("LOGGING_DEFAULT_LEVEL") or os.environ.get("LOG_DEFAULT_LEVEL")
    default_logger_output = os.environ.get("LOGGING_DEFAULT_HANDLER") or os.environ.get("LOG_DEFAULT_OUTPUT")

    if filename:
        filename = pathlib.Path(filename)

    if log_dir:
        log_dir = pathlib.Path(log_dir)
    else:
        if filename and filename.is_absolute():
            log_dir = filename.parent
        elif os.name == "nt" or "PYCHARM_HOSTED" in os.environ:
            log_dir = root_dir() / "log"
        else:
            log_dir = pathlib.Path("/var/log/", app_name)

    root.setLevel(logging.INFO)

    log_filename = os.environ.get("LOG_FILENAME", filename.name if filename else f"{app_name}.log")
    filename = log_dir / log_filename
    log_dir.mkdir(exist_ok=True)

    log_output = os.environ.get("LOG_OUTPUT") or os.environ.get("LOG_FORMAT") or "json,stderr"
    log_output = log_output.lower()
    root_handlers = log_output.split(",")
    root_handlers = [_normalize_name(handler_name) for handler_name in root_handlers]
    if not format_str:
        format_str = "%(asctime)s[%(levelname)7s][%(threadName)s][%(request_id)8s] %(message)s"

    _init_handlers(root, root_handlers, filename, format_str, rotate_mb, rotate_when, backup_count, log_level,
                   json_multiline, log_colored)

    if log_sql:
        try:
            from django.db import connection
            connection.force_debug_cursor = True  # only django specific import
        except ImportError:
            pass
        sql_logger = logging.getLogger("django.db.backends")
        sql_logger.setLevel(logging.DEBUG)
        sql_logger.addFilter(SQLExtraFilter())

    log_extra.init_extra_logger()
    log_extra.push_extra(progname=app_name)

    default_logger = logging.getLogger("default")
    if default_logger_level:
        default_logger.setLevel(default_logger_level)
        if default_logger_output:
            default_logger_handlers = default_logger_output.lower().split(",")
            default_logger_handlers = [_normalize_name(handler_name) for handler_name in default_logger_handlers]
            diff = set(default_logger_handlers) - set(root_handlers)
            if diff:
                _init_handlers(default_logger, diff, filename, format_str,
                               rotate_mb, rotate_when, backup_count,
                               default_logger_level, json_multiline, log_colored)
                default_logger.propagate = False
