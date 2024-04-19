import re
from common.domain.valueObject import ValueObject
from star.domain.userNombreInvalidException import UserNombreInvalidException

class UserNombre(ValueObject):
    def __init__(self, nombre: str):
      
        nombre = re.sub(r'[^a-zA-Z0-9_\-]', '_', nombre)
        self.nombre = nombre[:30]  # Limitar la longitud a 30 caracteres