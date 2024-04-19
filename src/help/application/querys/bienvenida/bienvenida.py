from common.application.query import Query

class Bienvenida(Query):
    def __init__(self,
                 username_name: str,
                 bot_name: str,
                 command_start: str):
        self.username_name = username_name
        self.bot_name = bot_name
        self.command_start = command_start
