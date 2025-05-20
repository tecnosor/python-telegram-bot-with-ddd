import json
import os
from common.domain.log.loggerService import LoggerService
from common.domain.secretsEngine.secretKeyNotFoundException import SecretKeyNotFoundException
from common.domain.secretsEngine.secretsEngineService import SecretsEngineService

class FileSecretsEngineService(SecretsEngineService):
    def __init__(self, logger: LoggerService):

        file_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Directorio actual del archivo: {file_dir}")

        project_root = os.path.abspath(os.path.join(file_dir, "..", "..", "..", ".."))
        print(f"Raíz del proyecto detectada: {project_root}")

        self.__path = os.path.join(project_root, ".secrets", "secrets.json")
        self.__path = os.path.normpath(self.__path)
        print(f"Ruta completa a secrets.json: {self.__path}")

        self.__logger = logger
        self.__key_value_secrets = {}
        self.__loadSecrets()


        self.__logger = logger
        self.__key_value_secrets = {}  # Aseguramos que la variable siempre exista
        self.__loadSecrets()

    def __loadSecrets(self):
        """Carga los secretos desde el archivo JSON."""
        try:
            if not os.path.exists(self.__path):
                print(f"❌ ERROR: No se encontró el archivo de secretos en {self.__path}")
                return
            
            print(f"📂 Intentando abrir: {self.__path}")  # 🔍 Ver la ruta exacta
            
            with open(self.__path, "r") as file:
                self.__key_value_secrets = json.load(file)
            
            print(f"✅ Secrets cargados correctamente: {list(self.__key_value_secrets.keys())}")  # 🔍 Muestra las claves cargadas
            self.__logger.log_info("Secrets loaded successfully.")

        except Exception as e:
            self.__logger.log_warning(f"❌ Failed to load secrets: {str(e)}")

    def get_secret(self, key: str):
        """Obtiene un secreto por clave."""
        print(f"🔍 Claves disponibles en secretos: {list(self.__key_value_secrets.keys())}")  # Muestra las claves disponibles
        print(f"🔍 Buscando clave '{key}' en secretos...")

        if key not in self.__key_value_secrets:
            raise SecretKeyNotFoundException(f"❌ ERROR: Secret key '{key}' not found.")
        
        return self.__key_value_secrets[key]
