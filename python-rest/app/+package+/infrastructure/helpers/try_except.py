# -*- coding: utf-8 -*-
import logging

from functools import wraps


def handler_except(method):
    @wraps(method)
    def method_wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except AttributeError as a:
            raise a
        except (Exception, ValueError) as e:
            logger = logging
            logger.basicConfig(
                    format='%(asctime)s [%(levelname)s] - %(name)s - %(message)s',
                    datefmt='[%Y/%m/%d %I:%M:%S %p]'
            )
            logger.error('=== Handler exception ===')
            logger.error(e)
            logger.error('=' * 25)
            return e
    return method_wrapper
