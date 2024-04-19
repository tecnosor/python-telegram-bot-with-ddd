from common.application.queryHandler import QueryHandler
from star.application.querys.getMyPosition.getMyPosition import GetMyPosition
from star.domain.position import Position
from star.domain.userId import UserId
from star.domain.userNotFoundException import UserNotFoundException
from star.domain.userRepository import UserRepository

class GetMyPositionHandler(QueryHandler):

    def __init__(self, 
                 user_repository: UserRepository):
        self.__user_repository = user_repository

    def handle(self, 
               input: GetMyPosition) -> Position:
        user_id = UserId(input.user_id)
        user = self.__user_repository.get_by_id(user_id.user_id)
        users = self.__user_repository.get_all()
        return users.get_posicion(user)