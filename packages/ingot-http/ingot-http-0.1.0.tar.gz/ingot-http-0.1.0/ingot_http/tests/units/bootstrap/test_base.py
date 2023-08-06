import typing as t

from ingots.tests.units.bootstrap import test_base

from ingot_http.bootstrap import IngotHttpBaseBuilder

__all__ = ("IngotHttpBaseBuilderTestCase",)


class IngotHttpBaseBuilderTestCase(test_base.BaseBuilderTestCase):
    """Contains tests for the IngotHttpBuilder class."""

    tst_cls: t.Type = IngotHttpBaseBuilder
    tst_entity_name: str = "ingot_http"
    tst_entity_name_upper: str = "INGOT_HTTP"
    tst_entity_name_class_name: str = "IngotHttp"
    tst_entity_description = (
        "Provides supporting the HTTP1.1 protocol for Ingots projects."
    )
