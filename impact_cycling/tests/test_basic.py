# -*- coding: utf-8 -*-
# impact-cycling (c) Caleb Braun

from nose.plugins.attrib import attr
from .mixins import DiamondTestCase


class BasicTestCase(DiamondTestCase):
    def test_basic(self):
        "ensure the minimum test works"
        assert True

    @attr("skip")
    def test_skip(self):
        assert False
