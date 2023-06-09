from collections import defaultdict
import random
import string

from user.models import User


class Sequence:
    ids = defaultdict(int)

    @classmethod
    def get(cls, name):
        cls.ids[name] += 1
        return cls.ids[name]
    


def generate_ascii_password(length: int) -> str:
    symbols = string.ascii_letters + string.digits
    password = ''.join([random.choice(symbols) for i in range(length)])
    return password

def get_test_username() -> str:
    return f"Test_username_{Sequence.get('username')}"

def get_test_user_password(lentgh: int = 12) -> str:
    return generate_ascii_password(lentgh)
