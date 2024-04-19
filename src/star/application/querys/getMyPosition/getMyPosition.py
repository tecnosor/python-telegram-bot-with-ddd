from common.application.query import Query

class GetMyPosition(Query):

    def __init__(self, user_id: int):
        self.user_id: int = user_id