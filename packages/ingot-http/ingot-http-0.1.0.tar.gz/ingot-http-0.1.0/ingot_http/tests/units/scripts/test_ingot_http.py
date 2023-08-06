import typing as t

from ingots.tests.units.scripts import test_base

from ingot_http.scripts.ingot_http import IngotHttpDispatcher

__all__ = ("IngotHttpDispatcherTestCase",)


class IngotHttpDispatcherTestCase(test_base.BaseDispatcherTestCase):
    """Contains tests for the IngotHttpDispatcher class and checks it."""

    tst_cls: t.Type = IngotHttpDispatcher
    tst_builder_name = "test"
