from django.contrib.auth.hashers import Argon2PasswordHasher


class LiteArgon2PasswordHasher(Argon2PasswordHasher):  # pylint: disable=too-few-public-methods
    memory_cost = 51200
    parallelism = 1
