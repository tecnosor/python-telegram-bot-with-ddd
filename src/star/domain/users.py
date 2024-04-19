from typing import List
from star.domain.position import Position
from star.domain.user import User
from star.domain.userNumeroStar import UserNumeroStar
from star.domain.usersNonUniqueNumeroStarException import UsersNonUniqueNumeroStarException

class Users:
    def __init__(self, users: List[User]):
        self.__validate_unique_numero_star(users)
        self.__users: List[User] = users

    def __validate_unique_numero_star(self, users: List[User]):
        numero_star_set = set()
        for user in users:
            if user.numero_star in numero_star_set:
                raise UsersNonUniqueNumeroStarException("El número Star debe ser único.")
            numero_star_set.add(user.numero_star)
    
    def get_posicion(self, user: User) -> Position:
        sorted_users = sorted(self.__users, key=lambda user: user.numero_star)
        position = next((i + 1 for i, user_in_list in enumerate(sorted_users) if user_in_list.user_id == user.user_id), None)
        valid_users = sum(1 for user in sorted_users if user.numero_star < UserNumeroStar.Ctes.MAX_NUM_STAR)
        return Position(position, valid_users)
    
    def is_numero_star_in_list(self, numero_star: int) -> bool:
        return numero_star in [u.numero_star for u in self.__users]
        
        