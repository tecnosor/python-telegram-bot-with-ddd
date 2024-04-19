from common.application.query import Query

class GetStarById(Query):

    def __init__(self, user_id: int):
        self.user_id: int = user_id