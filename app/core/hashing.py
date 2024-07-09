import bcrypt


def hashed_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hash_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hash_password.encode("utf-8"))
