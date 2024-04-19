from datetime import datetime
from common.application.command import Command

class RegisterMyStar(Command):
    def __init__(self, 
                 user_id: int,
                 nombre: str,
                 numero_star: int,
                 fecha_star: datetime):
        self.user_id = user_id
        self.nombre = nombre
        self.numero_star = numero_star
        self.fecha_star = fecha_star
