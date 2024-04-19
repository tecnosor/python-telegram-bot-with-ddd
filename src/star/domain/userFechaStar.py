from datetime import date, datetime, timedelta
from common.domain.valueObject import ValueObject
from star.domain.userFechaStarInvalidException import UserFechaStarInvalidException


class UserFechaStar(ValueObject):
    def __init__(self, fecha_star: datetime):
        now = datetime.now() + timedelta(minutes=1)
        if isinstance(fecha_star, date):
            time = datetime.min.time()
            fecha_star = datetime.combine(fecha_star, time)
            
        if fecha_star.year < 2016:
            raise UserFechaStarInvalidException(
                "La fecha Star no puede ser anterior a 2016."
            )

        if fecha_star > now:
            raise UserFechaStarInvalidException(
                "La fecha Star no puede ser posterior al día de hoy."
            )

        self.fecha_star = fecha_star
