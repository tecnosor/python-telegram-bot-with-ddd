import random
from typing import List
from star.domain.position import Position
from star.domain.user import User
from star.domain.userNumeroStar import UserNumeroStar
from star.domain.usersNonUniqueNumeroStarException import UsersNonUniqueNumeroStarException

class Users:
    def __init__(self, users: List[User]):
        self.__users: List[User] = []
        self.__assigned_numero_stars = set()
        self.__add_users(users)

    def __add_users(self, users: List[User]):
        for user in users:
            if user.numero_star in self.__assigned_numero_stars:
                user.numero_star = self.__generate_unique_numero_star()
            self.__assigned_numero_stars.add(user.numero_star)
            self.__users.append(user)

    def __generate_unique_numero_star(self) -> int:
        """Genera un número aleatorio único entre 99000 y 99999."""
        while True:
            new_numero_star = random.randint(99000, 99999)
            if new_numero_star not in self.__assigned_numero_stars:
                return new_numero_star

    def get_posicion(self, user: User) -> Position:
        sorted_users = sorted(self.__users, key=lambda user: user.numero_star)
        position = next((i + 1 for i, user_in_list in enumerate(sorted_users) if user_in_list.user_id == user.user_id), None)
        valid_users = sum(1 for user in sorted_users if user.numero_star < UserNumeroStar.Ctes.MAX_NUM_STAR)
        return Position(position, valid_users)
    
    def is_numero_star_in_list(self, numero_star: int) -> bool:
        return numero_star in self.__assigned_numero_stars
