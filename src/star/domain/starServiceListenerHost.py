from common.domain.log.loggerService import LoggerService
from common.domain.secretsEngine.secretsEngineService import SecretsEngineService
from common.domain.service import Service


class StarServiceListenerHost(Service):
    def run(self):
        raise NotImplementedError
