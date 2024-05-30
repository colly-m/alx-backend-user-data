#!/usr/bin/env python3
"""Module to encrypt passwds with bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Function to take string arg, converts to unicode
    Performs Hashing with hashpw
    Returns salted, hashed password as byte str
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Function to check if arg passed is the same as hashed and unhashed
    Returns boolean
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
