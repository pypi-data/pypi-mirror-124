from typing import Union


class PhinixExceptions(Exception):
    def __init__(self, func_name: str, message: Union[str, Exception]):
        self.func_name = func_name
        self.message = str(message)
        super().__init__(self.message)

    def __str__(self):
        return f'"{self.func_name}" -> {self.message}'


class RequestsExceptions(PhinixExceptions):
    pass


class StatusCodeError(PhinixExceptions):
    def __init__(self, func_name: str, status_code: int, message: Union[str, Exception]):
        self.func_name = func_name
        self.status_code = status_code
        self.message = message
        super().__init__(func_name, message)

    def __str__(self):
        return f'{self.func_name} | {self.status_code} -> {self.message}'


class JsonDecodingError(PhinixExceptions):
    def __init__(self, func_name: str, message: Union[str, Exception]):
        self.func_name = func_name
        self.message = message
        super().__init__(func_name, message)

    def __str__(self):
        return f'{self.func_name} -> {self.message}'


class InvalidResponse(PhinixExceptions):
    def __init__(self, func_name: str, message: Union[str, Exception]):
        self.func_name = func_name
        self.message = message
        super().__init__(func_name, message)

    def __str__(self):
        return f'{self.func_name} -> {self.message}'
