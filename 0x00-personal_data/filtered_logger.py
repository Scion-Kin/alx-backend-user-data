#!/usr/bin/env python3
''' This contains class and function definitons and a program '''

from typing import List
import mysql.connector
import os
import logging
import re


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    ''' returns the log message with specified fields obfuscated '''
    for f in fields:
        message = re.sub(fr'{f}=[^{separator}]*', f'{f}={redaction}', message)
    return message


def get_logger() -> logging.Logger:
    ''' returns a logger '''

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.propagate = False
    logger.addHandler(streamHandler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    ''' returns a connector to the database '''

    host = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_user = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_pwd = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_name = getenv('PERSONAL_DATA_DB_NAME', '')

    connection = mysql.connector.connect(host=host, user=db_user, port=3306,
                                         password=db_pwd, database=db_name)
    return connection


def main():
    ''' The main function '''

    db = get_db()
    logger, cursor = get_logger(), db.cursor()
    cursor.execute("SELECT * FROM users;")

    for row in cursor:
        row = ';'.join(("name=" + row[0], "email=" + row[1], "phone=" + row[2],
                        "ssn=" + row[3], "password=" + row[4], "ip" + row[5],
                        "last_login=" + str(row[6]), "user_agent=" + row[7]))
        logger.info(row)

    cursor.close(), db.close()


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


if __name__ == "__main__":
    main()
