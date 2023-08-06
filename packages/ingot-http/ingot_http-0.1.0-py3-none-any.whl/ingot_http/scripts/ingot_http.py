import typing as t
from logging import getLogger
from logging import INFO

from ingots.scripts.base import BaseDispatcher
from ingots.utils.logging import configure_startup_logging

if t.TYPE_CHECKING:
    from ingots.operations import BaseCliOperation  # noqa


__all__ = (
    "IngotHttpDispatcher",
    "main",
)


configure_startup_logging(
    default_level=INFO,
    format="%(levelname)s: %(message)s",
)
logger = getLogger(__name__)


class IngotHttpDispatcher(BaseDispatcher):

    name = "ingot_http"
    description = "The Ingot Http management CLI."
    cli_entities_classes: t.List[t.Type["BaseCliOperation"]] = []


def main():
    dispatcher = IngotHttpDispatcher.build()
    dispatcher.run()


if __name__ == "__main__":
    main()
