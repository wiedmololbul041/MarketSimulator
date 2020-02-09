import logging

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(logging.Formatter('[%(name)s][%(levelname)s]: %(message)s'))

        logger.addHandler(sh)

    return logger


if __name__ == '__main__':
    log = get_logger('logger_test')

    log.debug('Debug message')
    log.info('Info message')
    log.warning('Warning message')
    log.error('Error message')
    try:
        raise Exception("Exception message")
    except Exception as e:
        log.exception(e)
