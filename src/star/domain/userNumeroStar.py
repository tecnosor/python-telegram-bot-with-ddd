from common.domain.valueObject import ValueObject
from star.domain.userNumeroStarInvalidException import UserNumeroStarInvalidException


class UserNumeroStar(ValueObject):
    class Ctes:
        MAX_NUM_STAR: int = 99999
        MIN_NUM_STAR: int = 1

    def __init__(self, numero_star: int):
        if not isinstance(numero_star, int):
            raise UserNumeroStarInvalidException(
                "El número Star debe ser un número entero."
            )

        if numero_star < UserNumeroStar.Ctes.MIN_NUM_STAR:
            raise UserNumeroStarInvalidException(
                "El número Star debe ser mayor que cero."
            )

        if numero_star > UserNumeroStar.Ctes.MAX_NUM_STAR:
            raise UserNumeroStarInvalidException(
                "El número Star debe ser mayor que cero."
            )

        self.numero_star = numero_star
