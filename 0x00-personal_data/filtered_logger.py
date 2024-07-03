#!/usr/bin/env python3
''' This defines a function '''

from typing import List
import logging
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    ''' returns the log message with specified fields obfuscated '''
    for fi in fields:
        message = re.sub(r'{}=[^{}]*'.format(fi, separator), r'{}={}'.format(fi, redaction), message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        ''' formats incoming logs '''
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt
