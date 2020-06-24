import logging


class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ApplicationLogger(metaclass=SingletonMeta):
    def __init__(self):
        log_file_name = "app.log"
        self.__logger = logging.getLogger(log_file_name)
        self.__logger.setLevel(logging.INFO)
        self.__logger.propagate = False

        file_handler = logging.FileHandler(log_file_name)
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
        file_handler.setFormatter(formatter)
        self.__logger.addHandler(file_handler)

    def get_logger(self):
        return self.__logger
