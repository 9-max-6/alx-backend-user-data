#!/usr/bin/env python3
"""DB module
"""
import bcrypt


def _hash_password(password: str) -> str:
    """returns a hashed password"""
    if not isinstance(password, str):
        return
    return(
        bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )
    )
