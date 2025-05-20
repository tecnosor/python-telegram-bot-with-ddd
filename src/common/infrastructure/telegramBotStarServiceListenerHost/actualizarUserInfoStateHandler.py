import json
from enum import Enum
from telegram.ext import CallbackContext
from telegram import Update
from common.domain.log.loggerService import LoggerService
from common.domain.utils.date import Date
from star.application.commands.updateMyStar.updateMyStar import UpdateMyStar
from star.application.commands.updateMyStar.updateMyStarHandler import UpdateMyStarHandler
from star.domain.userFechaStarInvalidException import UserFechaStarInvalidException
from star.domain.userNotFoundException import UserNotFoundException
from star.domain.userRepository import UserRepository
from common.infrastructure.telegramBotStarServiceListenerHost.stateHandler import Statehandler

from pathlib import Path

class ActualizarUserInfoStatehandler(Statehandler):
    JSON_PATH = Path(__file__).resolve().parent.parent / "persistentmemorydb" / "users.json"

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
        user_id = str(update.message.from_user.id)  # Convierte el ID a string porque JSON usa claves string
        message_text = update.message.text

        print(f"🔄 Estado actual en __actualizar_numero_star: {self.get_state()}")  
        print(f"📩 Usuario {user_id} ingresó: {message_text}")  

        try:
            star_number = int(message_text)
        except ValueError:
            update.message.reply_text("❌ Por favor, ingresa un número válido.")
            return

        # Llamar a la función que actualiza el JSON
        if self.actualizar_numero_star(user_id, star_number):
            update.message.reply_text(f"✅ Número de Star actualizado a {star_number}.")
        else:
            update.message.reply_text("⚠️ Hubo un error al actualizar tu número de Star.")
        
        self.clear_state()  # Limpia el estado después de actualizar

    def actualizar_numero_star(self, user_id: str, nuevo_numero: int) -> bool:
        """Actualiza el número Star en el archivo JSON."""
        try:
            # 1️⃣ Cargar el JSON
            with open(self.JSON_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)

            # 2️⃣ Verificar si el usuario existe
            if user_id not in data:
                print(f"❌ Usuario {user_id} no encontrado.")
                return False

            # 3️⃣ Actualizar el número Star
            data[user_id]["numero_star"] = nuevo_numero

            # 4️⃣ Guardar los cambios en el JSON
            with open(self.JSON_PATH, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            print(f"✅ Número de Star actualizado a {nuevo_numero} para el usuario {user_id}.")
            return True

        except Exception as e:
            print(f"⚠️ Error al actualizar el JSON: {e}")
            return False

    def __actualizar_fecha_star(self, update: Update, context: CallbackContext):
        user_id      = int(update.message.from_user.id)
        message_text = update.message.text
        fecha        = Date(message_text).date

        update_my_star = UpdateMyStar(user_id=user_id, star_date=fecha)
        update_my_star_handler = UpdateMyStarHandler(self.__user_repo)

        try:
            update_my_star_handler.handle(update_my_star)
            update.message.reply_text('Fecha de entrada actualizada correctamente.')
        except UserNotFoundException:
            update.message.reply_text("No estás registrado como Star.")
        except Exception as e:
            if isinstance(e, (ValueError, UserFechaStarInvalidException)):
                update.message.reply_text('La fecha introducida no es válida')
            else:
                self.__logger.log_warning(str(e))
        finally:
            self.clear_state()

    def __option_selection(self, update: Update, context: CallbackContext):
        if update.message.chat.type != 'private':
            return

        message_text = update.message.text
        print(f"📩 Opción recibida: {message_text}")  # ✅ Verifica qué mensaje está llegando

        if message_text == "1":
            update.message.reply_text('Por favor, ingresa tu nuevo número de Star:')
            self.set_state(self.States.UPDATE_ACTUALIZAR_NUM_STAR.value)
            print(f"📌 Estado cambiado a: {self.States.UPDATE_ACTUALIZAR_NUM_STAR.value}")  # ✅ Verifica que el estado cambia

        elif message_text == "2":
            update.message.reply_text('Por favor, ingresa tu nueva fecha de entrada (formato dd/mm/yyyy):')
            self.set_state(self.States.UPDATE_ACTUALIZAR_FECHA_STAR.value)
            print(f"📌 Estado cambiado a: {self.States.UPDATE_ACTUALIZAR_FECHA_STAR.value}")  # ✅ Verifica el cambio de estado

        else:
            update.message.reply_text('❌ Opción inválida. Por favor, selecciona 1 o 2.')
