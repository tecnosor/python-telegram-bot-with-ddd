from common.domain.valueObject import ValueObject
from star.domain.userIdInvalidException import UserIdInvalidException


class UserId(ValueObject):
    def __init__(self, user_id: int):
        if user_id <= 0:
            raise UserIdInvalidException("El id de usuario debe de ser mayor que cero.")

        self.user_id = user_id
