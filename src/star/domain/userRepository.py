from common.domain.repository import Repository
from star.domain.user import User
from star.domain.users import Users


class UserRepository(Repository):
    def add(self, user_info: User):
        raise NotImplementedError

    def update(self, user_info: User):
        raise NotImplementedError

    def delete(self, user: User):
        raise NotImplementedError

    def get_by_id(self, user_id: int) -> User:
        raise NotImplementedError

    def get_all(self) -> Users:
        raise NotImplementedError
