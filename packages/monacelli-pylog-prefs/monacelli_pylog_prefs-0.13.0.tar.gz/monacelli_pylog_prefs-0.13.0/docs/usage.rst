=====
Usage
=====

To use monacelli_pylog_prefs in a project::

    import logging
    import pathlib

    import monacelli_pylog_prefs.logger


    def main():
        log = f"{pathlib.Path(__file__).stem}.log"
        monacelli_pylog_prefs.logger.setup(filename=log, stream_level=logging.DEBUG)
        logging.debug("all good")
        logging.warning("uh-oh")

    if __name__ == '__main__':
        main()
