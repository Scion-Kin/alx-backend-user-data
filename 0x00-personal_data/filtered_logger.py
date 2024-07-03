#!/usr/bin/env python3
''' This defines a function '''

from typing import List
import re


def filter_datum(fields: List[str], redaction: str, text: str, separator: str):
    ''' returns the log message with specified fields obfuscated '''
    for fi in fields:
        text = re.sub(r'{}=.+?{}'.format(fi, separator), r'{}={}{}'.format(fi, redaction, separator), text)
    return text
