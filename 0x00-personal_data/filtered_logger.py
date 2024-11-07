#!/usr/bin/python3
""" regex ing  """
from typing import List
import re


def filter_datum(fields, redaction, message, separator):
    """ filter datum """
    pattern = r'(' + '|'.join([f"{field}=[^ {separator}]+" for field in fields]) + r')'
    return re.sub(pattern, lambda x: f"{x.group().split('=')[0]}={redaction}", message)
