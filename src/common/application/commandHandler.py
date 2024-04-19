from common.application.command import Command
from common.application.handler import handler


class CommandHandler(handler):

    def __init__(self):
        raise NotImplementedError

    def handle(self, input: Command):
        raise NotImplementedError
