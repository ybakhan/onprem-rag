import logging
import os


def _configure_logging():
    if logging.getLogger().hasHandlers():
        return  # Someone else already configured

    level = os.environ.get("LOG_LEVEL", "INFO").upper()

    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s │ %(name)-28s │ %(levelname)-8s │ %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.getLogger(__name__).setLevel(logging.DEBUG)


# Only run configuration once when the package is first imported
_configure_logging()
