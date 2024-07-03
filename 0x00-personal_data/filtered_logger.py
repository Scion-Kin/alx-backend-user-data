#!/usr/bin/env python3
''' This defines a function '''

from typing import List
import re

patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}

def filter_datum(fields: List[str], redaction: str, message: str, separator: str):
    ''' returns the log message with specified fields obfuscated '''

    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)