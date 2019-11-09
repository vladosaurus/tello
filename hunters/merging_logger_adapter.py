# -*- coding: utf-8 -*-

from logging import LoggerAdapter


class MergingLoggerAdapter(LoggerAdapter):
    """
    Acts like logging.LoggerAdapter but instead of overwriting message extra
    it merges it together so that message extra has higher priority.
    """

    def process(self, msg, kwargs):
        extra = self.extra.copy()
        extra.update(kwargs.get("extra") or {})
        kwargs["extra"] = extra
        return msg, kwargs
