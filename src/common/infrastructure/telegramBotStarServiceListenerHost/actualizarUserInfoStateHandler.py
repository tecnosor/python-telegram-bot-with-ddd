from enum import Enum
from telegram.ext import CallbackContext
from telegram import Update
from common.domain.log.loggerService import LoggerService
from common.domain.utils.date import Date
from star.application.commands.updateMyStar.updateMyStar import UpdateMyStar
from star.application.commands.updateMyStar.updateMyStarHandler import UpdateMyStarHandler
from star.domain.userFechaStarInvalidException import UserFechaStarInvalidException
from star.domain.userNotFoundException import UserNotFoundException
from star.domain.userNumeroStar import UserNumeroStar
from star.domain.userNumeroStarInvalidException import UserNumeroStarInvalidException
from star.domain.userRepository import UserRepository
from star.domain.usersNonUniqueNumeroStarException import UsersNonUniqueNumeroStarException
from common.infrastructure.telegramBotStarServiceListenerHost.stateHandler import Statehandler

class ActualizarUserInfoStatehandler(Statehandler):
    class States(Enum):
        UPDATE_ACTUALIZAR_NUM_STAR   = "updateme_actualizar_numero_star"
        UPDATE_ACTUALIZAR_FECHA_STAR = "updateme_actualizar_fecha_star"
        UPDATE_SELECTION             = "updateme_selection"
    
    def __init__(self, logger: LoggerService, user_repository: UserRepository):
        dict_action = {
            self.States.UPDATE_ACTUALIZAR_NUM_STAR.value: self.__actualizar_numero_star,
            self.States.UPDATE_ACTUALIZAR_FECHA_STAR.value: self.__actualizar_fecha_star,
            self.States.UPDATE_SELECTION.value: self.__option_selection
        }
        self.__user_repo = user_repository
        super().__init__(logger, dict_action)

    def __actualizar_numero_star(self, update: Update, context: CallbackContext):
        user_id       = int(update.message.from_user.id)
        message_text = update.message.text
        star_number  = int(message_text)

        update_my_star = UpdateMyStar(user_id=user_id,
                                    star_number=star_number)
        update_my_star_handler = UpdateMyStarHandler(self.__user_repo)

        try:
            update_my_star_handler.handle(update_my_star)
            update.message.reply_text('Número de Star actualizado correctamente.')
        except UserNotFoundException:
            update.message.reply_text("No estás registrado como Star.")
        except UsersNonUniqueNumeroStarException:
            update.message.reply_text('Este número de Star ya está en uso. Por favor, elige otro.')
        except UserNumeroStarInvalidException:
            update.message.reply_text(f'Formato de número de Star inválido. El número debe estar entre {UserNumeroStar.Ctes.MIN_NUM_STAR} y {UserNumeroStar.Ctes.MAX_NUM_STAR}')
        finally:
            ## del context.user_data["state"]
            ## del context.user_data["handler"]
            # todo, revisar los del 
            self.clear_state()

    def __actualizar_fecha_star(self, update: Update, context: CallbackContext):
        user_id      = int(update.message.from_user.id)
        message_text = update.message.text
        fecha        = Date((message_text)).date

        update_my_star = UpdateMyStar(user_id=user_id,
                                      star_date=fecha)
        update_my_star_handler = UpdateMyStarHandler(self.__user_repo)

        try:
            update_my_star_handler.handle(update_my_star)
            update.message.reply_text('Fecha de entrada actualizada correctamente.')
        except UserNotFoundException:
            update.message.reply_text("No estás registrado como Star.")
        except Exception as e:
            if (isinstance(e, ValueError) or
                isinstance(e, UserFechaStarInvalidException)):
                update.message.reply_text('La fecha introducida no es válida')
            else:
                self.__logger.log_warning(str(e))
        finally:
            ## del context.user_data["state"]
            ## del context.user_data["handler"]
            # todo, revisar los del 
            self.clear_state()

    def __option_selection(self, update: Update, context: CallbackContext):
        if update.message.chat.type != 'private':
            return

        message_text = update.message.text
        if message_text == "1":
            update.message.reply_text('Por favor, ingresa tu nuevo número de Star:')
            self.set_state(self.States.UPDATE_ACTUALIZAR_NUM_STAR.value)
        elif message_text == "2":
            update.message.reply_text('Por favor, ingresa tu nueva fecha de entrada (formato dd/mm/yyyy):')
            self.set_state(self.States.UPDATE_ACTUALIZAR_FECHA_STAR.value)
        else:
            update.message.reply_text('Opción inválida. Por favor, selecciona 1 o 2.')
