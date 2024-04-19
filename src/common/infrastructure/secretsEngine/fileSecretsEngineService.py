import json
from common.domain.log.loggerService import LoggerService
from common.domain.secretsEngine.secretKeyNotFoundException import SecretKeyNotFoundException
from common.domain.secretsEngine.secretsEngineService import SecretsEngineService

class FileSecretsEngineService(SecretsEngineService):
    def __init__(self, 
                 logger: LoggerService):
        self.__path = "./.secrets/secrets.json"
        self.__logger = logger
        self.__key_value_secrets = {}
        self.__loadSecrets()

    def __loadSecrets(self):
        try:
            with open(self.__path, 'r') as file:
                self.__key_value_secrets = json.load(file)
                self.__logger.log_info("Secrets loaded successfully.")
        except Exception as e:
            self.__logger.log_warning(f"Failed to load secrets: {str(e)}")

    def get_secret(self, key: str):
        if key in self.__key_value_secrets:
            return self.__key_value_secrets[key]
        else:
            self.__logger.log_warning(f"Secret key '{key}' not found.")
            raise SecretKeyNotFoundException(f"Secret key '{key}' not found.")