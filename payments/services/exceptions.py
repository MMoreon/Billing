class ServiceError(Exception):
    """ошибка бизнес-логики"""


class ValidationServiceError(ServiceError):
    """Некорректные входные данные"""


class ConflictServiceError(ServiceError):
    """Конфликт состояния или идемпотентности"""


class NotFoundServiceError(ServiceError):
    """Объект не найден"""


class ForbiddenServiceError(ServiceError):
    """Операция запрещена"""
