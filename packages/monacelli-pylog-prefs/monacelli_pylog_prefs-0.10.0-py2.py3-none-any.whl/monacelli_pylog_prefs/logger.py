import logging
import logging.config
import logging.handlers


def get_file_handler(filename):

    if not filename:
        return None

    format_file = "[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    formatter_file = logging.Formatter(format_file)
    file_handler = logging.handlers.RotatingFileHandler(
        filename,
        mode="a",
    )
    file_handler.setFormatter(formatter_file)
    file_handler.setLevel(file_level)

    return file_handler


def get_stream_handler():
    format_stream = "{%(filename)s:%(lineno)d} %(levelname)s - %(message)s"  # console
    formatter_stream = logging.Formatter(format_stream)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter_stream)
    stream_handler.setLevel(stream_level)

    return stream_handler


def setup(filename=None, stream_level=logging.WARNING, file_level=logging.DEBUG):

    handlers = []

    hs = get_stream_handler()
    hf = get_file_handler(filename)

    if hs:
        handlers.append(hs)

    if hf:
        handlers.append(hf)

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=handlers,
    )
    logging.config.dictConfig({"version": 1, "disable_existing_loggers": True})
