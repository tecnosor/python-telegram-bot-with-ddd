from enum import Enum
from telegram import Update
from telegram.ext import CallbackContext

from common.domain.log.loggerService import LoggerService

class Statehandler:
    # abstract class, dont use for other proposals
    class States(Enum):
        pass

    def set_state(self, state):
        self.__valida_set_state(state)
        self.__context.user_data[self.__state_name] = state
        self.__state = state
    
    def clear_state(self):
        self.__context.user_data.pop(self.__state_name, None)
        self.__state = None

    def set_context(self, context: CallbackContext):
        self.__context = context
    
    def get_state(self):
        self.__state = self.__context.user_data[self.__state_name]
        return self.__state
    
    def __valida_set_state(self, state):
        return state in [s.value for s in self.States]
    
    def get_states(self):
        return self.States
    
    def __init__(self, logger: LoggerService, dictionary: dict = {}, state_name: str = "state"):
        self.__state_name = state_name
        self.__logger = logger
        self.__dict_action = dictionary
        
    def handle(self, update: Update, context: CallbackContext):
        if update.message.chat.type != 'private':
            return
        self.__context=context
        self.get_state()
        self.__logger.log_info(update)
        self.__dict_action.get(self.__state)(update, context)
