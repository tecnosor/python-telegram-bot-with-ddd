from datetime import datetime
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)
from telegram import Update

from common.domain.log.loggerService import LoggerService
from common.domain.secretsEngine.secretsEngineService import SecretsEngineService
from common.infrastructure.telegramBotStarServiceListenerHost.actualizarUserInfoStateHandler import (
    ActualizarUserInfoStatehandler,
)
from common.infrastructure.telegramBotStarServiceListenerHost.addUserInfoStateHandler import (
    AddUserInfoStateHandler,
)
from common.infrastructure.telegramBotStarServiceListenerHost.borrarHandler import (
    Borrarhandler,
)
from common.infrastructure.telegramBotStarServiceListenerHost.generalStateHandler import (
    GeneralStateHandler,
)

from help.application.querys.bienvenida.bienvenida import Bienvenida
from help.application.querys.bienvenida.bienvenidaHandler import BienvenidaHandler
from help.application.querys.start.start import Start
from help.application.querys.start.startHandler import StartHandler

from star.application.commands.registerMyStar.registerMyStar import RegisterMyStar
from star.application.commands.registerMyStar.registerMyStarHandler import (
    RegisterMyStarHandler,
)
from star.application.querys.getMyPosition.getMyPosition import GetMyPosition
from star.application.querys.getMyPosition.getMyPositionHandler import (
    GetMyPositionHandler,
)
from star.application.querys.getStarById.GetStarById import GetStarById
from star.application.querys.getStarById.GetStarByIdHandler import GetStarByIdHandler
from star.domain.operations import Operations
from star.domain.position import PosicionInvalidaException
from star.domain.starServiceListenerHost import StarServiceListenerHost
from star.domain.userAlreadyExistsException import UserAlreadyExistsException
from star.domain.userNotFoundException import UserNotFoundException
from star.domain.userNumeroStar import UserNumeroStar
from star.domain.userRepository import UserRepository


class TelegramBotStarServiceListenerHost(StarServiceListenerHost):
    def __init__(
        self,
        logger: LoggerService,
        secrets_engine: SecretsEngineService,
        user_repository: UserRepository,
    ):
        self.__logger = logger
        self.__secretsEngine = secrets_engine
        self.__user_repository = user_repository
        self.__borrarhandler = Borrarhandler(logger, user_repository)
        self.__generalStatehandler = GeneralStateHandler(
            logger, user_repository, "handler"
        )

    def run(self):
        self.__logger.log_info("... Init Telegram Bot ...")
        self.__load_secrets()
        self.__init()

    def __load_secrets(self):
        self.__logger.log_info("... Loading Secrets ...")
        self.__api_key = self.__secretsEngine.get_secret("TELEGRAM_API_KEY")

    def __init(self):
        self.__logger.log_info("... Loading Listeners ...")
        self.__updater = Updater(self.__api_key)
        updater = self.__updater
        operations = Operations()
        # Obtener el despachador para registrar los manejadores
        dispatcher = updater.dispatcher
        # Registrar los manejadores
        dispatcher.add_handler(CommandHandler("start", self.__start_comando))
        dispatcher.add_handler(
            CommandHandler(operations.Ctes.REGISTRAR.value, self.__registrar_comando)
        )
        dispatcher.add_handler(
            CommandHandler(
                operations.Ctes.MIPOSICION.value, self.__get_posicion_comando
            )
        )
        dispatcher.add_handler(
            CommandHandler(operations.Ctes.ACTUALIZAR.value, self.__actualizar_comando)
        )
        dispatcher.add_handler(
            CommandHandler(
                operations.Ctes.BORRAR.value, self.__borrarhandler.borrar_mi_star
            )
        )
        dispatcher.add_handler(
            CallbackQueryHandler(self.__borrarhandler.confirmacion_borrar)
        )
        dispatcher.add_handler(MessageHandler(Filters.status_update, self.__bienvenida))
        dispatcher.add_handler(
            MessageHandler(
                Filters.text & ~Filters.command, self.__generalStatehandler.handle
            )
        )
        dispatcher.add_error_handler(self.__error)

        # Iniciar el bot
        updater.start_polling()

        # Mantener el bot en ejecución hasta que se detenga manualmente
        updater.idle()

    # OK
    def __bienvenida(self, update: Update, context: CallbackContext) -> None:
        user_id = int(update.effective_chat.id)
        bot_name = context.bot.name
        for new_member in update.message.new_chat_members:
            name = (
                new_member.first_name
                if new_member.first_name is not None
                else new_member.username
            )
            bienvenida = Bienvenida(name, bot_name, "/start")
            bienvenida_handler = BienvenidaHandler()
            context.bot.send_message(user_id, bienvenida_handler.handle(bienvenida))

    # OK
    def __actualizar_comando(self, update: Update, context: CallbackContext) -> None:
        if update.message.chat.type != "private":
            return
        # aqui se podria validar antes de hacer nada, si el usuario existe, para mejorar la UX
        self.__logger.log_info(update)
        self.__set_context(context)
        update.message.reply_text(
            "¿Qué deseas actualizar?\n1. Número de Star\n2. Fecha de entrada"
        )
        self.__generalStatehandler.GetActualizarInfoStatehandler().set_state(
            ActualizarUserInfoStatehandler.States.UPDATE_SELECTION.value
        )
        self.__generalStatehandler.set_state(GeneralStateHandler.States.UPDATEAR.value)

    # OK
    def __set_context(self, context: CallbackContext):
        self.__generalStatehandler.set_context(context)

    # OK
    def __get_posicion_comando(self, update: Update, context: CallbackContext) -> None:
        print(f"📌 Recibido comando /MiPosicion de {update.message.from_user.id}")

        if update.message.chat.type != "private":
            print("⚠️ Comando rechazado: No es chat privado")
            return
        
        user_id = int(update.message.from_user.id)
        get_my_position = GetMyPosition(user_id)
        get_my_position_handler = GetMyPositionHandler(self.__user_repository)

        try:
            position = get_my_position_handler.handle(get_my_position)
            print(f"✅ Usuario encontrado. Posición: {position.posicion}/{position.total_usuarios}")
            update.message.reply_text(
                f"{update.message.from_user.first_name}, tu posición en la lista de Star es: {position.posicion} de {position.total_usuarios}"
            )
        except Exception as e:
            print(f"❌ Error en /MiPosicion: {e}")  # Debugging
            update.message.reply_text(
                f"Lo siento, primero tienes que añadirme a la lista con /{Operations.Ctes.REGISTRAR.value}"
            )


    # OK
    def __start_comando(self, update: Update, context: CallbackContext) -> None:
        if not self.__isPrivate(update):
            return

        start = Start()
        start_handler = StartHandler()
        mensaje = start_handler.handle(start)
        update.message.reply_text(
            f"Hola {update.message.from_user.first_name}!\n\n{mensaje}."
        )

    # OK
    def __isPrivate(self, update: Update):
        if update.message.chat.type != "private":
            update.message.reply_text(
                f"Hola {update.message.from_user.first_name}, por favor escribeme por privado con /start para no ensuciar en el grupo."
            )
            return False
        else:
            return True

    # OK
    def __registrar_comando(self, update: Update, context: CallbackContext) -> None:
        if update.message.chat.type != "private":
            return
        self.__logger.log_info(update)
        user_id = int(update.message.from_user.id)
        username = (
            update.message.from_user.first_name
            if update.message.from_user.first_name is not None
            else update.message.from_user.username
        )

        register_my_star = RegisterMyStar(user_id, username, UserNumeroStar.Ctes.MAX_NUM_STAR, datetime.today())
        register_my_star_handler = RegisterMyStarHandler(self.__user_repository)

        try:
            register_my_star_handler.handle(register_my_star)

            update.message.reply_text("Por favor, dime tu número de Star:")
            self.__generalStatehandler.set_context(context)
            self.__generalStatehandler.set_state(GeneralStateHandler.States.ADD.value)
            self.__generalStatehandler.GetCrearUserInfoStatehandler().set_state(
                AddUserInfoStateHandler.States.ADD_NUM_STAR.value
            )
        except UserAlreadyExistsException:
            update.message.reply_text(
                f"Lo siento {username}, ya estás en la lista. Puedes probar a actualizar tu información con /{Operations.Ctes.ACTUALIZAR.value} ó consultar tu posición con /{Operations.Ctes.MIPOSICION.value}"
            )

    # OK
    def __error(self, update: Update, context: CallbackContext) -> None:
        self.__generalStatehandler.clear_state()
        self.__logger.log_warning(f"Update {update} caused error {context.error}")
