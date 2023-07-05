import re


def name_valid(name: str) -> bool:
    if 2<= len(name) <= 30 and name.isalpha() and name.istitle():
        return True
    return False


def password_valid(password: str) -> bool:
    pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$')
    return re.match(pattern_password, password) is not None

