from enum import Enum


class Operations:
    class Ctes(Enum):
        REGISTRAR = "RegistrarMiStar"
        ACTUALIZAR = "ActualizarMiStar"
        BORRAR = "BorrarMiStar"
        MIPOSICION = "MiPosicionStar"

    def operations(self):
        return [
            self.Ctes.REGISTRAR,
            self.Ctes.ACTUALIZAR,
            self.Ctes.BORRAR,
            self.Ctes.MIPOSICION,
        ]
