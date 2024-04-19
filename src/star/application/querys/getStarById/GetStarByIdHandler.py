from common.application.queryHandler import QueryHandler
from star.application.querys.getStarById.GetStarById import GetStarById
from star.domain.userId import UserId
from star.domain.userRepository import UserRepository

class GetStarByIdHandler(QueryHandler):
    def __init__(self, 
                 user_repository: UserRepository):
        self.__user_repository = user_repository

    def handle(self, 
               input: GetStarById):
        user_id = UserId(input.user_id)
        user = self.__user_repository.get_by_id(user_id.user_id)
        return user