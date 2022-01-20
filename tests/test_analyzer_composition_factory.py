#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2020 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     wmeijer221 <w.meijer.5@student.rug.nl>
#

import unittest

from graal.backends.core.cocom.compositions.composition_lizard_file import LIZARD_FILE, CATEGORY_COCOM_LIZARD_FILE
from graal.backends.core.cocom.compositions.composition_lizard_repository import LIZARD_REPOSITORY, CATEGORY_COCOM_LIZARD_REPOSITORY
from graal.backends.core.cocom.compositions.composition_scc_file import SCC_FILE, CATEGORY_COCOM_SCC_FILE
from graal.backends.core.cocom.compositions.composition_scc_repository import SCC_REPOSITORY, CATEGORY_COCOM_SCC_REPOSITORY

from graal.backends.core.composer import Composer
from graal.backends.core.analyzer_composition_factory import AnalyzerCompositionFactory
from graal.graal import GraalError

from base_analyzer import TestCaseAnalyzer


class TestAnalyzerCompositionFactory(TestCaseAnalyzer):
    """Tests AnalyzerCompositionFactory"""

    target_package = "graal.backends.core.cocom.compositions"

    def test_constructor(self):
        """Tests constructor"""

        fac = AnalyzerCompositionFactory(self.target_package)
        self.assertGreater(len(fac.get_categories()), 0)

        with self.assertRaises(GraalError):
            fac = AnalyzerCompositionFactory("unknown.package")

    def test_get_categories(self):
        """Tests get categories."""

        fac = AnalyzerCompositionFactory(self.target_package)

        cats = fac.get_categories()
        self.assertEqual(len(cats), 4)
        self.assertIn(CATEGORY_COCOM_LIZARD_FILE, cats)
        self.assertIn(CATEGORY_COCOM_LIZARD_REPOSITORY, cats)
        self.assertIn(CATEGORY_COCOM_SCC_FILE, cats)
        self.assertIn(CATEGORY_COCOM_SCC_REPOSITORY, cats)

    def test_get_composer(self):
        """Tests Get Composer method and the returned compositions."""

        fac = AnalyzerCompositionFactory(self.target_package)
        cats = fac.get_categories()

        for cat in cats:
            composer = fac.get_composer(cat)

            self.assertTrue(composer)
            self.assertTrue(issubclass(type(composer), Composer))

            self.assertEqual(type(composer.get_kind()), str)
            self.assertEqual(type(composer.get_category()), str)
            self.assertEqual(type(composer.get_composition()), list)

    def test_category_from_kind(self):
        """Test get category from kind method."""

        fac = AnalyzerCompositionFactory(self.target_package)

        self.assertEqual(fac.get_category_from_kind(LIZARD_FILE), CATEGORY_COCOM_LIZARD_FILE)
        self.assertEqual(fac.get_category_from_kind(LIZARD_REPOSITORY), CATEGORY_COCOM_LIZARD_REPOSITORY)
        self.assertEqual(fac.get_category_from_kind(SCC_FILE), CATEGORY_COCOM_SCC_FILE)
        self.assertEqual(fac.get_category_from_kind(SCC_REPOSITORY), CATEGORY_COCOM_SCC_REPOSITORY)

    def test_unknown(self):
        """Tests methods with unknown category."""

        fac = AnalyzerCompositionFactory(self.target_package)

        with self.assertRaises(GraalError):
            fac.get_composer("unknown")

        with self.assertRaises(GraalError):
            fac.get_category_from_kind("unknown")


if __name__ == "__main__":
    unittest.main()
