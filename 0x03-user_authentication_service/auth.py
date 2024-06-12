#!/usr/bin/env python3
"""Module to define a method that take password and retun bytes"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Function to generate a salt to turn the input args into bytes"""
    salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hash_pwd
