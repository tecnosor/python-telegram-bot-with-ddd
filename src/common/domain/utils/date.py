from datetime import datetime
from common.domain.valueObject import ValueObject


class Date(ValueObject):
    def __init__(self, date: str):
        self.date = self.__str_a_fecha(date)

    def __str_a_fecha(self, 
                    fecha_str: str) -> datetime.date:
        try:
            fecha = datetime.strptime(fecha_str, '%d/%m/%Y').date()
            return fecha
        except ValueError:
            raise ValueError("Formato de fecha incorrecto. Utiliza el formato dd/mm/yyyy.")
