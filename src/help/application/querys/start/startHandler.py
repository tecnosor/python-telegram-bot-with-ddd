from common.application.queryHandler import QueryHandler
from help.application.querys.start.start import Start as StartApplication
from help.domain.start import Start as StartDomain

class StartHandler(QueryHandler):
    def __init__(self):
        # do nothing
        pass
    
    def handle(self, start: StartApplication) -> str:
        start_domain = StartDomain()
        return start_domain.get_info_commands()