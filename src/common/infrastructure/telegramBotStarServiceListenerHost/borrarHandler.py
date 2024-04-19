from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from common.domain.log.loggerService import LoggerService
from star.application.commands.deleteMyStar.deleteMyStar import DeleteMyStar
from star.application.commands.deleteMyStar.deleteMyStarHandler import (
    DeleteMyStarHandler,
)
from star.domain.userNotFoundException import UserNotFoundException
from star.domain.userRepository import UserRepository


class Borrarhandler:

    def __init__(self, logger: LoggerService, user_repository: UserRepository):
        self.__BORRAR_SI = "BORRAR_SI"
        self.__BORRAR_NO = "BORRAR_NO"
        self.__logger = logger
        self.__user_repo = user_repository

    def borrar_mi_star(self, update: Update, context: CallbackContext) -> None:
        if update.message.chat.type != "private":
            return
        # Creamos un teclado para confirmar la acción
        keyboard = [
            [
                InlineKeyboardButton("Sí", callback_data=self.__BORRAR_SI),
                InlineKeyboardButton("No", callback_data=self.__BORRAR_NO),
            ]
        ]
        self.__logger.log_info(update)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "¿Estás seguro que deseas borrar tu usuario?", reply_markup=reply_markup
        ) # ojo, esto puede validar si el usuario esta registrado como Star, antes de dejar seguir, para mejorar la UX

    # Manejador de la confirmación del usuario
    def confirmacion_borrar(self, update: Update, context: CallbackContext) -> None:
        self.__logger.log_info(update)
        query = update.callback_query
        user_id = int(update.effective_user.id)
        username = (
            query.message.from_user.first_name
            if query.message.from_user.first_name is not None
            else query.message.from_user.username
        )

        if query.data == self.__BORRAR_SI:
            try:
                delete_my_star_use_case = DeleteMyStar(user_id)
                delete_my_star_use_case_handler = DeleteMyStarHandler(self.__user_repo)
                delete_my_star_use_case_handler.handle(delete_my_star_use_case)
                self.__logger.log_info(f"USUARIO: {username} BORRADO")
                query.edit_message_text("Tu usuario ha sido borrado exitosamente.")
            except UserNotFoundException:
                query.edit_message_text("No estás registrado como Star.")
        else:
            query.edit_message_text("Operación cancelada.")
