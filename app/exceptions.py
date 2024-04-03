class AppException(Exception): ...


class PermissionError(AppException):
    def __init__(self, msg: str = "권한이 없습니다.") -> None:
        super().__init__(msg)


class ValidationError(AppException):
    def __init__(self, msg: str = "유효하지 않습니다.") -> None:
        super().__init__(msg)


class NotFoundError(AppException):
    def __init__(self, msg: str = "존재하지 않습니다.") -> None:
        super().__init__(msg)
