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

    def __log(self, mensaje: str):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensaje}")

    def add(self, user_info: User):
        self.update(user_info)

    def update(self, user_info: User) -> None:
        self.__log(f"📝 Intentando actualizar usuario {user_info.user_id} con numero_star {user_info.numero_star}")
        
        if user_info.user_id in self.dict_user_info:
            self.__log("✅ Usuario encontrado, actualizando...")
        else:
            self.__log("❌ ERROR: Usuario no encontrado en la base de datos en memoria")

        self.dict_user_info[user_info.user_id] = user_info
        self.__save_to_file()

        # Verificar si se guardó correctamente
        with open(self.__file_name, "r") as archivo:
            data = json.load(archivo)
            if str(user_info.user_id) in data:
                self.__log(f"✅ Confirmado: el usuario {user_info.user_id} fue guardado en el JSON.")
            else:
                self.__log(f"❌ ERROR: El usuario {user_info.user_id} no se guardó en el JSON.")

    def delete(self, user: User):
        self.dict_user_info.pop(user.user_id, None)
        self.__save_to_file()

    def get_by_id(self, user_id: int) -> User:
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
        try:
            with open(self.__file_name, "r") as archivo:
                dict_user_info_serializable = json.load(archivo)
                for user_id, user_info in dict_user_info_serializable.items():
                    self.dict_user_info[int(user_id)] = User(
                        UserNombre(user_info["nombre"]),
                        UserNumeroStar(int(user_info["numero_star"])),
                        UserFechaStar(datetime.strptime(user_info["fecha_star"], "%d/%m/%Y")),
                        UserId(int(user_info["user_id"])),
                    )
            self.__log(f"📌 Usuarios cargados desde JSON: {self.dict_user_info}")
        except Exception as e:
            self.__log(f"❌ Error cargando usuarios desde JSON: {e}")
