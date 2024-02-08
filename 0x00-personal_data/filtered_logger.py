#!/usr/bin/env python3
"""
Method file
"""
from datetime import datetime
import re
import logging
import os
from typing import List, Union

import mysql.connector
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def format(fields: List[str], redaction: str, message: str,
           separator: str) -> str:
    """The method that filters the fields"""
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]*",
                         f"{field}={redaction}",
                         message)
    return message


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """The method that filters the fields"""
    return format(fields, redaction, message, separator)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(" \
             "message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """the init method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """This is the method that formats a record and obfuscates it"""
        original_message = record.getMessage()
        filtered_message = filter_datum(self.fields, self.REDACTION,
                                        original_message, self.SEPARATOR)
        record.msg = filtered_message
        return super().format(record)


def get_logger() -> logging.Logger:
    """get the logger formatted with the fields"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    sh = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger


def get_db() -> Union[PooledMySQLConnection, MySQLConnectionAbstract]:
    """Connect to the MySQL database and return a connection object."""
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', 'william667')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME', 'my_db')

    conn = mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name
    )
    return conn


def main() -> None:
    """the main file where the program begins"""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")

    for row in cursor:
        key_value_pairs = [f"{key}={row[key]}" for key in row.keys()]
        filtered_values = filter_datum(PII_FIELDS,
                                       RedactingFormatter.REDACTION,
                                       '; '.join(key_value_pairs),
                                       RedactingFormatter.SEPARATOR)
        formatted_row = ', '.join(
            f"{key}={row[key]}" for key in row.keys() if
            key not in PII_FIELDS)
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[HOLBERTON] user_data INFO {current_datetime}:" \
                      f" {filtered_values};" \
                      f" {formatted_row}"
        print(log_message)


if __name__ == "__main__":
    main()
