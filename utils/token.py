from base64 import b64encode, b64decode

from utils.random_emoji import random_emoji


class Token:
    @staticmethod
    def encode(source: str) -> str:
        return b64encode(bytes(source, 'utf8'))

    @staticmethod
    def decode(source: str) -> str:
        return str(b64decode(source), 'utf8')

    @staticmethod
    def generate():
        token = ''

        for _ in range(10):
            token += random_emoji()

        return token
