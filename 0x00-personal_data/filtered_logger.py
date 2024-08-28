#!/usr/bin/env python3
"""module: function: filter_datum"""
import re
import sys
import logging
import os
import mysql.connector
from mysql.connector import errorcode
from typing import List, Tuple


PII_FIELDS: Tuple = (
    "email",
    "phone",
    "ssn",
    "password",
    "ip",
)

def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
) -> str:
    """
    A function to obfuscate a log message
    steps:
    1. split all with ;
    2. list comprehension to replace matched pattern
    3. Join again with the separator
    4. Return
    """
    ps = message.split(separator)
    pattern = "|".join(re.escape(field) + r'=(.*)' for field in fields)
    ob_parts = [re.sub(pattern, (
        lambda match: match.group(0).split("=")[0]+"="+f"{redaction}"
        ), p) for p in ps]
    return separator.join(ob_parts)


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
        """a function to implement redaction"""
        original_message = super().format(record)
        return filter_datum(
            self.fields,
            self.REDACTION,
            original_message,
            self.SEPARATOR
            )

def get_logger() -> logging.Logger:
    """a function to return a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(RedactingFormatter)
    logger.addHandler(stream_handler)

    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """A function to return a DB connector"""
    try:
        cnx = mysql.connector.connect(
            user=os.getenv('PERSONAL_DATA_DB_USERNAME', "root"),
            password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ""),
            host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
            database=os.getenv('PERSONAL_DATA_DB_NAME')
            )
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
