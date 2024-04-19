from common.application.query import Query

class QueryHandler:
    def __init__(self):
        raise NotImplementedError
    
    def handle(self, input: Query):
        raise NotImplementedError