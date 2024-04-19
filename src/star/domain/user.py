from star.domain.userFechaStar import UserFechaStar
from star.domain.userId import UserId
from star.domain.userNombre import UserNombre
from star.domain.userNumeroStar import UserNumeroStar


class User:
    def __init__(
        self,
        nombre: UserNombre,
        numero_star: UserNumeroStar,
        fecha_star: UserFechaStar,
        user_id: UserId,
    ):
        self.nombre = nombre.nombre
        self.numero_star = numero_star.numero_star
        self.fecha_star = fecha_star.fecha_star
        self.user_id = user_id.user_id

    def to_json(self):
        return {
            "nombre": self.nombre,
            "numero_star": self.numero_star,
            "fecha_star": self.fecha_star.strftime("%d/%m/%Y"),
            "user_id": self.user_id,
        }
