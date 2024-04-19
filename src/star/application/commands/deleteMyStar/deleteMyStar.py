from common.application.command import Command

class DeleteMyStar(Command):
    def __init__(self, user_id: int):
        self.user_id: int = user_id

