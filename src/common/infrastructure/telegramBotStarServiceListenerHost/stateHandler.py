from enum import Enum
from telegram import Update
from telegram.ext import CallbackContext
from common.domain.log.loggerService import LoggerService

class Statehandler:
    # abstract class, dont use for other proposals
    class States(Enum):
        pass

    def __init__(self, logger: LoggerService, dictionary: dict = {}, state_name: str = "state"):
        self.__state_name = state_name
        self.__logger = logger
        self.__dict_action = dictionary
        self.__context = None  # Inicializamos el contexto para evitar AttributeError

    def set_state(self, state):
        if not self.__valida_set_state(state):
            return  # Evita asignar un estado inválido
        self.__context.user_data[self.__state_name] = state
        self.__state = state

    def clear_state(self):
        if self.__context:  # Evita error si __context no está definido
            self.__context.user_data.pop(self.__state_name, None)
        self.__state = None

    def set_context(self, context: CallbackContext):
        self.__context = context

    def get_state(self):
        if self.__context and self.__state_name in self.__context.user_data:
            self.__state = self.__context.user_data[self.__state_name]
        else:
            self.__state = None  # Si el estado no existe, evitamos KeyError
        return self.__state

    def __valida_set_state(self, state):
        return state in [s.value for s in self.States]

    def get_states(self):
        return self.States

    def handle(self, update: Update, context: CallbackContext):
        if update.message.chat.type != 'private':
            return  # Si no es chat privado, no hacemos nada

        self.set_context(context)  # Asignamos el contexto
        state = self.get_state()  # Obtenemos el estado actual

        self.__logger.log_info(update)

        if state:
            action = self.__dict_action.get(state, lambda u, c: None)
            action(update, context)  # Ejecutamos la acción si existe
