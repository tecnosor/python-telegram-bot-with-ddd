from common.application.queryHandler import QueryHandler
from help.application.querys.bienvenida.bienvenida import Bienvenida as BienvenidaQuery
from help.domain.bienvenida import Bienvenida

class BienvenidaHandler(QueryHandler):
    def __init__(self):
        # do nothing
        pass
    def handle(self, input: BienvenidaQuery):
        bienvenida = Bienvenida()
        return bienvenida.get_mensaje_bienvenida( input.username_name,
                                                input.bot_name,
                                                input.command_start)