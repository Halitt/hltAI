import logging

def setup_logger(log_file: str = "app.log"):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def log_info(message: str):
    logging.info(message)

def log_error(message: str):
    logging.error(message)