from common.domain.service import Service

class LoggerService(Service):

    def log_warning(self, message: str):
        raise NotImplementedError
    
    def log_info(self, message: str):
        raise NotImplementedError