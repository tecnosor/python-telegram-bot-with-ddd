from common.application.commandHandler import CommandHandler
from star.application.commands.deleteMyStar.deleteMyStar import DeleteMyStar
from star.domain.userNotFoundException import UserNotFoundException
from star.domain.userRepository import UserRepository

class DeleteMyStarHandler(CommandHandler):
    def __init__(self,
                 user_repository: UserRepository):
        self.__user_repository = user_repository

    def handle(self, input: DeleteMyStar):
        user = self.__user_repository.get_by_id(input.user_id)
        self.__user_repository.delete(user)