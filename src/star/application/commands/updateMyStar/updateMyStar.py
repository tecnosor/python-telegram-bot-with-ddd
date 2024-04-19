from datetime import datetime
from common.application.command import Command


class UpdateMyStar(Command):
    def __init__(self, 
                 user_id: int,
                 star_number: int =-1,
                 star_date: datetime = None):
        self.user_id: int = user_id
        self.star_number: int = star_number
        self.star_date: datetime = star_date