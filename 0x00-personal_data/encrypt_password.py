#!/usr/bin/env python3
"""
bcrypting file
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ hash a password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """To validate if the cde matches"""
    password_bytes = password.encode('utf-8')

    # Use bcrypt to check if the provided password matches the hashed
    # password
    return bcrypt.checkpw(password_bytes, hashed_password)
