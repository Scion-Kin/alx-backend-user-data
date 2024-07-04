#!/usr/bin/env python3
''' This defines a function '''

from typing import List
import csv
import logging
import re


PII_FIELDS = ("email", "phone", "ssn", "password", "ip")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    ''' returns the log message with specified fields obfuscated '''
    for f in fields:
        message = re.sub(fr'{f}=[^{separator}]*', f'{f}={redaction}', message)
    return message


def get_logger() -> logging.Logger:
    ''' defines a new logger '''

    logger = logging.Logger('user_data')
    logger.setLevel(logging.INFO)
    streamHandler = logging.StreamHandler().setFormatter(RedactingFormatter)
    logger.addHandler(streamHandler)
    return logger

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        ''' formats incoming logs '''
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
