from star.domain.posicionInvalidaException import PosicionInvalidaException


class Position:
    def __init__(self, posicion: int, total: int):
        if (
            posicion is None
            or total is None
            or total < 1
            or posicion > total
            or posicion < 1
        ):
            raise PosicionInvalidaException()
        self.posicion = (
            posicion  ## esto deberia tener getters y setters, no ser publico ** nota
        )
        self.total_usuarios = total
