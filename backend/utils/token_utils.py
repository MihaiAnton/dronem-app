"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   30.04.2020 20:50
"""

import bcrypt


def hash_token(token: str) -> str:
    return bcrypt.hashpw(token.encode('utf-8'), bcrypt.gensalt()).decode()


def check_token(token: str, hashed: str) -> bool:
    return bcrypt.checkpw(token.encode('utf-8'), hashed.encode('utf-8'))
