from common.domain.valueObject import ValueObject


class Bienvenida(ValueObject):

    def get_mensaje_bienvenida(self, 
                             nombre_usuario: str, 
                             nombre_bot: str, 
                             nombre_comando: str) -> str:
        return f"Bienvenido al grupo {nombre_usuario}! Soy {nombre_bot}. Escribeme por privado con el comando {nombre_comando} si quieres saber algo sobre tu posición Star."