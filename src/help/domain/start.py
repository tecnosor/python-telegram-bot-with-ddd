from common.domain.valueObject import ValueObject
from star.domain.operations import Operations

class Start(ValueObject):
    def __init__(self):
        self.__operations = Operations()

    def get_info_commands(self)-> str:
        opciones = [
            f'- Para añadirte como Star, utiliza el comando /{self.__operations.Ctes.REGISTRAR.value}',
            f'- Para actualizar tu información de Star, utiliza el comando /{self.__operations.Ctes.ACTUALIZAR.value}',
            f'- Para borrar tu registro como Star, utiliza el comando /{self.__operations.Ctes.BORRAR.value}',
            f'- Para consultar tu posición en la lista de Stars, utiliza el comando /{self.__operations.Ctes.MIPOSICION.value}'
        ]
        return "\n".join(opciones)
        
