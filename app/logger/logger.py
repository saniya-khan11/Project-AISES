import logging
from pathlib import Path


class AISESLogger:

    _logger = None

    @classmethod
    def get_logger(cls):

        if cls._logger is not None:
            return cls._logger

        log_dir = Path("outputs/logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / "aises.log"

        logger = logging.getLogger("AISES")

        logger.setLevel(logging.INFO)

        logger.handlers.clear()

        formatter = logging.Formatter(

            "%(asctime)s | %(levelname)s | %(message)s",

            datefmt="%Y-%m-%d %H:%M:%S"

        )

        file_handler = logging.FileHandler(

            log_file,

            encoding="utf-8"

        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        logger.addHandler(console_handler)

        cls._logger = logger

        return logger