from typing import List


class Character:
    def __init__(self, char: str) -> None:
        if not isinstance(char, str):
            raise ValueError("Character must be str")
        if len(char) > 1:
            raise ValueError("Character must have length of 1")

        self.char = char

    def __str__(self) -> str:
        return self.char

    def __repr__(self) -> str:
        return self.char


class Message:
    def __init__(self, string: List[Character]) -> None:
        if not isinstance(string, list):
            raise ValueError("string must be a list of Characters")

        for each in string:
            if not isinstance(each, Character):
                raise ValueError("Each element of string must be a Characters")

        self.string = string

    def __str__(self) -> str:

        return "".join(list(map(lambda x: x.char, self.string)))

    def __repr__(self) -> str:
        return "".join(list(map(lambda x: x.char, self.string)))


class Hello:
    def __init__(self, message: Message):
        if not isinstance(message, Message):
            raise ValueError("message must be a Message")

        self.message = message

    def print(self):
        print(self.message)
