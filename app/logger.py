import logging

# Set up the logger
logger = logging.getLogger("todo_logger")
logger.setLevel(logging.DEBUG)

# Console handler with formatter
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)

# Avoid duplicate logs if re-imported
if not logger.hasHandlers():
    logger.addHandler(console_handler)
