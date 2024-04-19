from common.application.commandHandler import CommandHandler
from star.application.commands.registerMyStar.registerMyStar import RegisterMyStar
from star.domain.user import User
from star.domain.userAlreadyExistsException import UserAlreadyExistsException
from star.domain.userFechaStar import UserFechaStar
from star.domain.userId import UserId
from star.domain.userNombre import UserNombre
from star.domain.userNotFoundException import UserNotFoundException
from star.domain.userNumeroStar import UserNumeroStar
from star.domain.userRepository import UserRepository


class RegisterMyStarHandler(CommandHandler):
    def __init__(self, 
                 user_repository: UserRepository):
        self.__user_repository = user_repository

    def handle(self, 
               input: RegisterMyStar):
        user = User(UserNombre(input.nombre),
                    UserNumeroStar(input.numero_star),
                    UserFechaStar(input.fecha_star),
                    UserId(input.user_id))
        
        try:
            user = self.__user_repository.get_by_id(user.user_id)
            raise UserAlreadyExistsException("User with ID {} already exists".format(user.user_id))
        except UserNotFoundException:
            self.__user_repository.add(user)