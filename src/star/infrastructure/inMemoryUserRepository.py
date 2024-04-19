from datetime import datetime
import json
from star.domain.user import User
from star.domain.userFechaStar import UserFechaStar
from star.domain.userId import UserId
from star.domain.userNombre import UserNombre
from star.domain.userNotFoundException import UserNotFoundException
from star.domain.userNumeroStar import UserNumeroStar
from star.domain.userRepository import UserRepository
from star.domain.users import Users


class InMemoryUserRepository(UserRepository):
    def __init__(self, file_name):
        self.dict_user_info: dict[int, User] = {}
        self.__file_name = file_name
        self.__load_from_file()

    def add(self, user_info: User):
        self.update(user_info)

    def update(self, user_info: User) -> None:
        self.dict_user_info[user_info.user_id] = user_info
        self.__save_to_file()

    def delete(self, user: User):
        self.dict_user_info.pop(user.user_id,None)
        self.__save_to_file()

    def get_by_id(self, user_id: int) -> User:
        """
        Ojo ojito, al devolver directamente user, si lo manipulamos durante la capa de aplicacion etc, se manipulara tambien directamente en la base de datos de memoria
        La manera de resolver esto es generando un clon.

        return User(UserId(user.user_id),...)

        Asi nos aseguramos que la unica manera de hacer cambios es a través del repositorio.
        """
        user = self.dict_user_info.get(user_id, None)
        if user is None:
            raise UserNotFoundException()
        return User(
            UserNombre(user.nombre),
            UserNumeroStar(user.numero_star),
            UserFechaStar(user.fecha_star),
            UserId(user.user_id),
        )

    def get_all(self) -> Users:
        users_prov = list(self.dict_user_info.values())
        users_copy = []
        for user in users_prov:
            users_copy.append(
                User(
                    UserNombre(user.nombre),
                    UserNumeroStar(user.numero_star),
                    UserFechaStar(user.fecha_star),
                    UserId(user.user_id),
                )
            )
        return Users(users_copy)

    def __save_to_file(self):
        dict_user_info_serializable = {
            user_id: user_info.to_json()
            for user_id, user_info in self.dict_user_info.items()
        }
        with open(self.__file_name, "w") as archivo:
            json.dump(dict_user_info_serializable, archivo)

    def __load_from_file(self):
        with open(self.__file_name, "r") as archivo:
            dict_user_info_serializable = json.load(archivo)
            for user_id, user_info in dict_user_info_serializable.items():
                self.dict_user_info[int(user_id)] = User(
                    UserNombre(user_info["nombre"]),
                    UserNumeroStar(int(user_info["numero_star"])),
                    UserFechaStar(
                        datetime.strptime(user_info["fecha_star"], "%d/%m/%Y")
                    ),
                    UserId(int(user_info["user_id"])),
                )
