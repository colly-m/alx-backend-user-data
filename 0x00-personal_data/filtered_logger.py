#!/usr/bin/env python3
"""Module to return an obfuscated log message"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    Function to get an obfuscated message
    Args:
        fields: list of string representing all fields
        reduction: string reping what to obfuscate
        message: string reping a log line
        separator: string reping characters for separating fields
    """
    pattern = "|".join(f"(?<={field}=)[^{separator}]+" for field in fields)
    return re.sub(pattern, redaction, message)
