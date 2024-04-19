from enum import Enum
from telegram.ext import CallbackContext
from common.domain.log.loggerService import LoggerService
from common.infrastructure.telegramBotStarServiceListenerHost.actualizarUserInfoStateHandler import ActualizarUserInfoStatehandler
from common.infrastructure.telegramBotStarServiceListenerHost.stateHandler import Statehandler
from common.infrastructure.telegramBotStarServiceListenerHost.addUserInfoStateHandler import AddUserInfoStateHandler
from star.domain.operations import Operations
from star.domain.userRepository import UserRepository

class GeneralStateHandler(Statehandler):
    class States(Enum):
        UPDATEAR = Operations.Ctes.ACTUALIZAR.value
        ADD = Operations.Ctes.REGISTRAR.value

    def __init__(self, 
                 logger: LoggerService, 
                 user_repository: UserRepository,
                 state_name: str = "state"):
        self.__actualizarUserInfoStatehandler = ActualizarUserInfoStatehandler(logger, user_repository)
        self.__crearUserInfoStatehandler = AddUserInfoStateHandler(logger, user_repository)

        dict_action = {
            self.States.UPDATEAR.value: self.__actualizarUserInfoStatehandler.handle,
            self.States.ADD.value: self.__crearUserInfoStatehandler.handle,
        }
        super().__init__(logger, dict_action, state_name)

    def set_context(self, context: CallbackContext):
        self.__actualizarUserInfoStatehandler.set_context(context)
        self.__crearUserInfoStatehandler.set_context(context)
        return super().set_context(context)
    
    def clear_state(self):
        self.__actualizarUserInfoStatehandler.clear_state()
        self.__crearUserInfoStatehandler.clear_state()
        super().clear_state()
    
    def GetActualizarInfoStatehandler(self) -> ActualizarUserInfoStatehandler:
        return self.__actualizarUserInfoStatehandler
    
    def GetCrearUserInfoStatehandler(self) -> AddUserInfoStateHandler:
        return self.__crearUserInfoStatehandler