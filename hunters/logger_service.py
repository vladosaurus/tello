# -*- coding: utf-8 -*-

import logging
from functools import lru_cache

import graypy

from .merging_logger_adapter import MergingLoggerAdapter


def extra_logger(name="drones", level=logging.DEBUG, extra=None):
    logger_ = _build_logger(name)
    logger_.setLevel(level)
    return MergingLoggerAdapter(logger_, extra or {})


@lru_cache(maxsize=None)
def _build_logger(name):
    """
    :type name: str
    :rtype: logging.Logger
    """
    # Return a logger with the specified name or, if name is None, return a logger which is the root logger of the hierarchy.
    logger_ = logging.getLogger(name)

    # Returns a new instance of the StreamHandler class.
    # If stream is specified, the instance will use it for logging output; otherwise, sys.stderr will be used.
    handler = logging.StreamHandler()
    logger_.addHandler(handler)  # Add the specified handler to this logger

    logger_.addHandler(graypy.GELFUDPHandler('tello.uvidime.xyz', 12216))

    return logger_
