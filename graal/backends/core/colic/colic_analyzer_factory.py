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
#     Valerio Cosentino <valcos@bitergia.com>
#     inishchith <inishchith@gmail.com>
#

from graal.graal import GraalError

from graal.backends.core.colic.compositions.composition_nomos import *
from graal.backends.core.colic.compositions.composition_scancode import *
from graal.backends.core.colic.compositions.composition_scancode_cli import *


class CoLicAnalyzerFactory:
    """Factory class for Analyzer Compositions"""

    version = '0.1.0'

    def __init__(self):
        self.__load_compositions()

    def __load_compositions(self):
        self.compositions = {}
        self.__add(CompositionNomos())
        self.__add(CompositionScancode())
        self.__add(CompositionScancodeCli())

    def __add(self, composer):
        """Adds composer to the factory"""

        self.compositions[composer.get_category()] = composer
        self.compositions[composer.get_kind()] = composer

    def build(self, category):
        """Returns composition of analyzers"""

        composer = self.get_composer(category)
        composition = composer.get_composition()

        return composition

    def get_composer(self, category):
        """Returns composer object corresponding with category"""

        if not category in self.compositions:
            raise GraalError(cause=f"Unknown category {category}")

        return self.compositions[category]

    def get_categories(self):
        """Returns all considered categories"""

        return self.compositions.keys()
