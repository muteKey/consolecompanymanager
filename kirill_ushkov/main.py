from ConsoleDBManager.controllers.menu_controller import MenuController
from ConsoleDBManager.views.views import MenuInitialView
from logging.config import dictConfig

logging_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'detailed': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'app-info.log',
            'mode': 'w',
            'level': 'INFO',
            'formatter': 'detailed',
        },
        'errors': {
            'class': 'logging.FileHandler',
            'filename': 'app-errors.log',
            'mode': 'w',
            'level': 'ERROR',
            'formatter': 'detailed',
        },
    },
    'loggers': {
        'ConsoleDBManager.controllers.database_controller': {
            'handlers': ['file', 'errors'],
            'level': 'INFO',
        },
        'ConsoleDBManager.views.views': {
            'handlers': ['file', 'errors'],
            'level': 'INFO',
        }
    }
}

if __name__ == "__main__":
    dictConfig(logging_config)

try:
    menuController = MenuController(MenuInitialView())
except KeyboardInterrupt:
    print()
    print("Goodbye!")
