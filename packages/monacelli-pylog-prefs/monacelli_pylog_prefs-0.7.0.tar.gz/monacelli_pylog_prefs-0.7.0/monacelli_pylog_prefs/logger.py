import logging
import logging.config
import logging.handlers


def setup(filename=None, stream_level=logging.WARNING, file_level=logging.DEBUG):
    format_file = "[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    formatter_file = logging.Formatter(format_file)
    file_handler = logging.handlers.RotatingFileHandler(
        filename,
        mode="a",
    )
    file_handler.setFormatter(formatter_file)
    file_handler.setLevel(file_level)

    format_stream = "{%(filename)s:%(lineno)d} %(levelname)s - %(message)s"  # console
    formatter_stream = logging.Formatter(format_stream)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter_stream)
    stream_handler.setLevel(stream_level)

    handlers = [stream_handler]
    if filename:
        handlers.append(file_handler)

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=handlers,
    )
    logging.config.dictConfig({"version": 1, "disable_existing_loggers": True})
