from common.domain.log.loggerService import LoggerService
from common.domain.service import Service


class SecretsEngineService(Service):

    def get_secret(self, key: str):
        raise NotImplementedError