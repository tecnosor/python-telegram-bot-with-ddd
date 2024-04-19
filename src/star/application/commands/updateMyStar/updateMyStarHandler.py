from common.application.commandHandler import CommandHandler
from star.application.commands.updateMyStar.updateMyStar import UpdateMyStar
from star.domain.userFechaStar import UserFechaStar
from star.domain.userId import UserId
from star.domain.userNumeroStar import UserNumeroStar
from star.domain.userRepository import UserRepository
from star.domain.usersNonUniqueNumeroStarException import UsersNonUniqueNumeroStarException

class UpdateMyStarHandler(CommandHandler):
    def __init__(self, 
                 user_repository: UserRepository
                 ):
        self.__user_repository: UserRepository = user_repository

    def handle(self, 
               input: UpdateMyStar):
        user_id = UserId(input.user_id)
        user = self.__user_repository.get_by_id(user_id.user_id)
        users = self.__user_repository.get_all()
        
        if input.star_number > -1:
            numero_star = UserNumeroStar(input.star_number).numero_star
            if users.is_numero_star_in_list(numero_star):
                raise UsersNonUniqueNumeroStarException("El número Star debe ser único.")
            user.numero_star = numero_star
        if input.star_date is not None:
            user.fecha_star = UserFechaStar(input.star_date).fecha_star
        
        self.__user_repository.update(user)