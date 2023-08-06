from logging import getLogger

from ingots.bootstrap.base import BaseBuilder

import ingot_http as package

__all__ = ("IngotHttpBaseBuilder",)


logger = getLogger(__name__)


class IngotHttpBaseBuilder(BaseBuilder):

    package = package
