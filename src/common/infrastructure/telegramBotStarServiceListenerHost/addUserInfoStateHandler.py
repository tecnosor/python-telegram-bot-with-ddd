from datetime import datetime
from enum import Enum
from telegram.ext import CallbackContext
from telegram import Update
from common.domain.utils.date import Date
from common.infrastructure.telegramBotStarServiceListenerHost.stateHandler import (
    Statehandler,
)
from star.application.commands.updateMyStar.updateMyStar import UpdateMyStar
from star.application.commands.updateMyStar.updateMyStarHandler import (
    UpdateMyStarHandler,
)
from star.domain.operations import Operations
from star.domain.userFechaStarInvalidException import UserFechaStarInvalidException
from star.domain.userNotFoundException import UserNotFoundException
from star.domain.userNumeroStarInvalidException import UserNumeroStarInvalidException
from star.domain.userRepository import UserRepository
from star.domain.users import UsersNonUniqueNumeroStarException


class AddUserInfoStateHandler(Statehandler):
    class States(Enum):
        ADD_NUM_STAR = "add_numero_star"
        ADD_FECHA_STAR = "add_fecha_star"

    def __init__(self, logger, user_repo: UserRepository):
        dict_action = {
            self.States.ADD_NUM_STAR.value: self.__add_numero_star,
            self.States.ADD_FECHA_STAR.value: self.__add_fecha_star,
        }
        self.__user_repo = user_repo
        super().__init__(logger, dict_action)

    def get_states(self):
        return self.States

    def __add_numero_star(self, update: Update, context: CallbackContext):
        user_id = int(update.message.from_user.id)
        message_text = update.message.text
        star_number = int(message_text)

        update_my_star = UpdateMyStar(user_id=user_id, star_number=star_number)
        update_my_star_handler = UpdateMyStarHandler(self.__user_repo)

        try:
            update_my_star_handler.handle(update_my_star)
            hoy = datetime.today().strftime(f'%d/%m/%Y')
            update.message.reply_text(f"Por último, dime tu fecha de entrada de la forma dd/mm/yyyy, por ejemplo: {hoy}")
            self.set_state(self.States.ADD_FECHA_STAR.value)
        except UserNotFoundException:
            update.message.reply_text("No estás registrado como Star.")
            self.clear_state()
        except UsersNonUniqueNumeroStarException:
            update.message.reply_text(
                "Este número de Star ya está en uso. Por favor, elige otro."
            )
            self.clear_state()
        except Exception as e:
            if isinstance(e, ValueError) or isinstance(
                e, UserNumeroStarInvalidException
            ):
                update.message.reply_text(
                    "Formato de número de Star inválido. Introduce un número entero."
                )
            else:
                raise e
            self.clear_state()

    def __add_fecha_star(self, update: Update, context: CallbackContext):
        user_id = int(update.message.from_user.id)
        message_text = update.message.text
        fecha = Date((message_text)).date

        update_my_star = UpdateMyStar(user_id=user_id, star_date=fecha)
        update_my_star_handler = UpdateMyStarHandler(self.__user_repo)

        try:
            update_my_star_handler.handle(update_my_star)
            update.message.reply_text(f"Felicidades, ya puedes consultar tu posición con /{Operations.Ctes.MIPOSICION.value}")
        except UserNotFoundException:
            update.message.reply_text("No estás registrado como Star.")
        except Exception as e:
            if isinstance(e, ValueError) or isinstance(
                e, UserFechaStarInvalidException
            ):
                update.message.reply_text("La fecha introducida no es válida")
            else:
                raise e
        finally:
            self.clear_state()
