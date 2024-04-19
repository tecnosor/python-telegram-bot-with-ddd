from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Messagehandler, Filters, CallbackQueryHandler
import logging
import json
from logging.handlers import TimedRotatingFilehandler

# Configurar el registro para mensajes de nivel INFO
logger_info = logging.getLogger("info_logger")
logger_info.setLevel(logging.INFO)

info_handler = TimedRotatingFilehandler("audit.log", when="midnight", interval=1, backupCount=7)
info_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger_info.addhandler(info_handler)

# Configurar el registro para mensajes de nivel WARNING
logger_warning = logging.getLogger("warning_logger")
logger_warning.setLevel(logging.WARNING)

warning_handler = TimedRotatingFilehandler("errors.log", when="midnight", interval=1, backupCount=7)
warning_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger_warning.addhandler(warning_handler)

def borrar_mi_star(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type != 'private':
        return
    # Creamos un teclado para confirmar la acción
    keyboard = [
        [
            InlineKeyboardButton("Sí", callback_data='borrar_si'),
            InlineKeyboardButton("No", callback_data='borrar_no')
        ]
    ]
    logger_info.info(update)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('¿Estás seguro que deseas borrar tu usuario?', reply_markup=reply_markup)

# Manejador de la confirmación del usuario
def confirmacion_borrar(update: Update, context: CallbackContext) -> None:
    logger_info.info(update)
    query = update.callback_query
    chat_id = query.message.chat_id

    if query.data == 'borrar_si':
        if chat_id in dict_user_info.keys():
            logger_info.info(f"USUARIO: {json.dumps(dict_user_info[chat_id].to_json())} BORRADO")
            del dict_user_info[chat_id]
            guardar_usuarios()
            query.edit_message_text("Tu usuario ha sido borrado exitosamente.")
        else:
            query.edit_message_text("No estás registrado como Star.")
    else:
        query.edit_message_text("Operación cancelada.")


# Almacenar la información en memoria
class UserInfo:
    def __init__(self, 
                 nombre: str, 
                 numero_star: int, 
                 fecha_star: datetime, 
                 user_id: str):
        self.numero_star = numero_star
        self.nombre = nombre
        self.fecha_star = fecha_star
        self.user_id = user_id

    def to_json(self):
        return {
            "nombre": self.nombre,
            "numero_star": self.numero_star,
            "fecha_star": self.fecha_star.strftime('%d/%m/%Y'),  # Convertir datetime a string
            "user_id": self.user_id
        }
    
dict_user_info: dict[int, UserInfo] = {}


def guardar_usuarios():
    dict_user_info_serializable = {chat_id: user_info.to_json() for chat_id, user_info in dict_user_info.items()}
    with open('usuarios.json', 'w') as archivo:
        json.dump(dict_user_info_serializable, archivo)

def cargar_usuarios():
    try:
        with open('usuarios.json', 'r') as archivo:
            dict_user_info_serializable = json.load(archivo)
            dict_user_info = {}
            for chat_id, user_info_data in dict_user_info_serializable.items():
                fecha_star = datetime.strptime(user_info_data['fecha_star'], '%d/%m/%Y').date()  # Convertir string a datetime
                user_info = UserInfo(
                    nombre=user_info_data['nombre'],
                    numero_star=int(user_info_data['numero_star']),
                    fecha_star=datetime.strptime(user_info_data['fecha_star'], '%d/%m/%Y').date(),
                    user_id=int(user_info_data['user_id'])
                )
                dict_user_info[int(chat_id)] = user_info
            return dict_user_info
    except FileNotFoundError:
        return {}

# Llama a esta función al inicio del bot para cargar el diccionario de usuarios
dict_user_info = cargar_usuarios()


def str_a_fecha(fecha_str: str) -> datetime.date:
    try:
        fecha = datetime.strptime(fecha_str, '%d/%m/%Y').date()
        return fecha
    except ValueError:
        raise ValueError("Formato de fecha incorrecto. Utiliza el formato dd/mm/yyyy.")

# Manejador del comando /ActualizarMiStar
def actualizar_mi_star(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type != 'private':
        return
    logger_info.info(update)
    chat_id = int(update.message.from_user.id)

    if chat_id not in dict_user_info.keys():
        update.message.reply_text('Aún no estás registrado como Star. Utiliza /RegistrarMiStar para registrarte.')
        return

    update.message.reply_text('¿Qué deseas actualizar?\n1. Número de Star\n2. Fecha de entrada')
    # Establecer el siguiente paso de la conversación
    context.user_data["state"] = "actualizar_opcion"
    context.user_data["handler"] = "updateme_select"


# Manejador del mensaje de texto para actualizar el número de Star
def actualizar_numero_star(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type != 'private':
        return
    logger_info.info(update)
    message_text = update.message.text
    if message_text == "1":
        update.message.reply_text('Por favor, ingresa tu nuevo número de Star:')
        context.user_data["state"] = "actualizar_numero_star"
        context.user_data["handler"] = "updateme"
        return  # Salir de la función para evitar que se ejecute el siguiente manejador
    elif message_text == "2":
        update.message.reply_text('Por favor, ingresa tu nueva fecha de entrada (formato dd/mm/yyyy):')
        context.user_data["state"] = "actualizar_fecha_entrada"
        context.user_data["handler"] = "updateme"
        return  # Salir de la función para evitar que se ejecute el siguiente manejador
    else:
        update.message.reply_text('Opción inválida. Por favor, selecciona 1 o 2.')


# Manejador del mensaje de texto para actualizar el número de Star
def updateme_soystar_text_handler(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type != 'private':
        return
    chat_id = int(update.message.from_user.id)
    message_text = update.message.text

    state = context.user_data.get("state", None)
    if state == "actualizar_numero_star":
        try:
            nuevo_numero_star = int(message_text)
            # Comprobar si el número de Star ya está en uso
            if any(user.numero_star == nuevo_numero_star for user in dict_user_info.values()):
                update.message.reply_text('Este número de Star ya está en uso. Por favor, elige otro.')
                return
            dict_user_info[chat_id].numero_star = nuevo_numero_star
            update.message.reply_text('Número de Star actualizado correctamente.')
            guardar_usuarios()
        except ValueError:
            update.message.reply_text('Formato de número de Star inválido. Introduce un número entero.')
        finally:
            del context.user_data["state"]
            del context.user_data["handler"]
    elif state == "actualizar_fecha_entrada":
        try:
            nueva_fecha_entrada = str_a_fecha(message_text)
            dict_user_info[chat_id].fecha_star = nueva_fecha_entrada
            update.message.reply_text('Fecha de entrada actualizada correctamente.')
            guardar_usuarios()
        except ValueError as e:
            update.message.reply_text("Formato de fecha incorrecto")
        finally:
            del context.user_data["state"]
            del context.user_data["handler"]
    else: 
        pass


# Manejador del comando /start
def start(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type != 'private':
        update.message.reply_text(f'Hola {update.message.from_user.first_name}, por favor escribeme por privado con /start para no ensuciar en el grupo.')
        return
    logger_info.info(update)
    opciones = [
        f'- Para añadirte como Star, utiliza el comando /{CommandsCTEs.CTE_COMMANDC_ADD_MY_STAR}',
        f'- Para actualizar tu información de Star, utiliza el comando /{CommandsCTEs.CTE_COMMANDC_UPDATE_MY_STAR}',
        f'- Para borrar tu registro como Star, utiliza el comando /{CommandsCTEs.CTE_COMMANDC_CLEAR_MY_STAR}',
        f'- Para consultar tu posición en la lista de Stars, utiliza el comando /{CommandsCTEs.CTE_COMMANDQ_MY_POSITION_STAR}'
    ]
    mensaje = "\n".join(opciones)
    update.message.reply_text(f'Hola {update.message.from_user.first_name}!\n\n{mensaje}.\n\nRecuerda que puedes hablarme en privado si quieres mantener esta información en oculto.')

# Manejador del comando /MiPosicionStar
def mi_posicion_star(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type != 'private':
        return
    chat_id = str(update.message.from_user.id)

    # Ordenar el diccionario por numero_star
    sorted_users = sorted(dict_user_info.values(), key=lambda x: x.numero_star)

    # Encontrar la posición del usuario actual
    position = next((i + 1 for i, user in enumerate(sorted_users) if str(user.user_id) == chat_id), None)

    if position and position < 9999:
        valid_users = sum(1 for user in sorted_users if user.numero_star < 9999)
        update.message.reply_text(f'{update.message.from_user.first_name}, tu posición en la lista de Star es: {position} de {valid_users}')
    else:
        update.message.reply_text(f'Lo siento, primero tienes que añadirte a la lista o actualizar tu número star para poder consultar tu posicion. /{CommandsCTEs.CTE_COMMANDC_ADD_MY_STAR} ó /{CommandsCTEs.CTE_COMMANDC_UPDATE_MY_STAR}')

# Manejador del comando /addme-soystar
def addme_soystar(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type != 'private':
        return
    logger_info.info(update)
    chat_id = int(update.message.from_user.id)
    username = update.message.from_user.username if update.message.from_user.username is None else update.message.from_user.first_name
    if chat_id not in dict_user_info.keys():
        dict_user_info[chat_id] = UserInfo(username, 9999, datetime.today(), str(chat_id))
    else:
        update.message.reply_text(f'Lo siento {username}, ya estás en la lista. Puedes probar a actualizar tu información con /{CommandsCTEs.CTE_COMMANDC_UPDATE_MY_STAR} ó consultar tu posición con /{CommandsCTEs.CTE_COMMANDQ_MY_POSITION_STAR}')
        return

    update.message.reply_text('Por favor, dime tu número de Star:')
    # Establecer el siguiente paso de la conversación
    context.user_data["state"] = "star_number"
    context.user_data["handler"] = "addme"

# Función para saludar cuando alguien se une al grupo
def welcome_new_member(update: Update, context: CallbackContext):

    chat_id = update.effective_chat.id
    bot_name = context.bot.name
    for new_member in update.message.new_chat_members:
        context.bot.send_message(chat_id, f"Bienvenido al grupo {new_member.first_name}! Soy {bot_name}. Escribeme por privado con el comando /start si quieres saber algo sobre tu posición Star")


# Manejador del mensaje de texto
def addme_soystar_text_handler(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type != 'private':
        return
    chat_id = int(update.message.from_user.id)
    message_text = update.message.text

    # Obtener el estado actual de la conversación
    state = context.user_data.get("state", None)

    if state == "star_number":
        star_number = int(message_text)
        # Comprobar si el número de Star ya está en uso
        if dict_user_info and star_number in [user.numero_star for user in dict_user_info.values()]:
            update.message.reply_text('Este número de Star ya está en uso. Por favor, elige otro.')
            return
        dict_user_info[chat_id].numero_star = star_number
        hoy = datetime.today().strftime(f'%d/%m/%Y')
        update.message.reply_text(f'Por último, dime tu fecha de entrada de la forma dd/mm/yyyy, por ejemplo: {hoy}')
        context.user_data["state"] = "fecha_entrada"
    elif state == "fecha_entrada":
        try:
            fecha = str_a_fecha(message_text)
            dict_user_info[chat_id].fecha_star = fecha
            update.message.reply_text(f'¡Gracias por registrarte como Star {update.message.from_user.first_name}!')

            # Reiniciar el estado de la conversación
            del context.user_data["state"]
            guardar_usuarios()
        except ValueError as e:
            update.message.reply_text(str(e))

        # Reiniciar el estado de la conversación
        del context.user_data["state"]
        del context.user_data["handler"]
    else:
        update.message.reply_text('No entiendo lo que quieres decir.')


def generic_text_handler(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type != 'private':
        return
    logger_info.info(update)
    if context.user_data["handler"] == "addme":
        addme_soystar_text_handler(update, context)
    elif context.user_data["handler"] == "updateme":
        updateme_soystar_text_handler(update, context)
    elif context.user_data["handler"] == "updateme_select":
        actualizar_numero_star(update, context)

# Manejador de errores
def error(update: Update, context: CallbackContext) -> None:
    logger_warning.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    # Inicializar el bot
    updater = Updater(CTE_API_TOKEN)

    # Obtener el despachador para registrar los manejadores
    dispatcher = updater.dispatcher

    # Registrar los manejadores
    dispatcher.add_handler(CommandHandler(CommandsCTEs.CTE_COMMANDC_START, start))
    dispatcher.add_handler(CommandHandler(CommandsCTEs.CTE_COMMANDC_ADD_MY_STAR, addme_soystar))
    dispatcher.add_handler(CommandHandler(CommandsCTEs.CTE_COMMANDQ_MY_POSITION_STAR, mi_posicion_star))
    dispatcher.add_handler(CommandHandler(CommandsCTEs.CTE_COMMANDC_UPDATE_MY_STAR, actualizar_mi_star))
    dispatcher.add_handler(CommandHandler(CommandsCTEs.CTE_COMMANDC_CLEAR_MY_STAR, borrar_mi_star))
    dispatcher.add_handler(CallbackQueryHandler(confirmacion_borrar))
    dispatcher.add_handler(Messagehandler(Filters.status_update, welcome_new_member))

    dispatcher.add_handler(Messagehandler(Filters.text & ~Filters.command, generic_text_handler))
    dispatcher.add_error_handler(error)

    # Iniciar el bot
    updater.start_polling()

    # Mantener el bot en ejecución hasta que se detenga manualmente
    updater.idle()



class CommandsCTEs:
    CTE_COMMANDC_START = "start"
    CTE_COMMANDC_ADD_MY_STAR = "RegistrarMiStar"
    CTE_COMMANDC_UPDATE_MY_STAR = "ActualizarMiStar"
    CTE_COMMANDC_CLEAR_MY_STAR = "BorrarMiStar"
    CTE_COMMANDQ_MY_POSITION_STAR = "MiPosicionStar"


## CON


if __name__ == '__main__':
    main()