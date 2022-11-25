from django.contrib.auth.hashers import Argon2PasswordHasher


class LiteArgon2PasswordHasher(Argon2PasswordHasher):  # pylint: disable=too-few-public-methods
    parallelism = 1
