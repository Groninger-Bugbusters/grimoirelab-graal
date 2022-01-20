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

import logging
import os
from graal.backends.core.covuln.covuln_analyzer_factory import CoVulnAnalyzerFactory

from graal.graal import (
    Graal,
    GraalCommand,
    GraalError,
    GraalRepository,
    DEFAULT_WORKTREE_PATH,
)

from perceval.utils import DEFAULT_DATETIME, DEFAULT_LAST_DATETIME

CATEGORY_COVULN = "code_vulnerabilities"
CATEGORIES = [CATEGORY_COVULN]

logger = logging.getLogger(__name__)


class CoVuln(Graal):
    """CoVuln backend.

    This class extends the Graal backend. It gathers
    insights about security vulnerabilities in Python code.

    :param uri: URI of the Git repository
    :param gitpath: path to the repository or to the log file
    :param worktreepath: the directory where to store the working tree
    :param exec_path: path of the executable to perform the analysis
    :param entrypoint: the entrypoint of the analysis
    :param in_paths: the target paths of the analysis
    :param out_paths: the paths to be excluded from the analysis
    :param details: if enable, it returns fine-grained results
    :param tag: label used to mark the data
    :param archive: archive to store/retrieve items

    :raises RepositoryError: raised when there was an error cloning or
        updating the repository.
    """

    version = "0.3.1"

    def __init__(
        self,
        uri,
        git_path,
        worktreepath=DEFAULT_WORKTREE_PATH,
        exec_path=None,
        entrypoint=None,
        in_paths=None,
        out_paths=None,
        details=False,
        tag=None,
        archive=None,
    ):
        super().__init__(
            uri,
            git_path,
            worktreepath,
            exec_path=exec_path,
            entrypoint=entrypoint,
            in_paths=in_paths,
            out_paths=out_paths,
            details=details,
            tag=tag,
            archive=archive,
        )

        self.__factory = CoVulnAnalyzerFactory()
        self.CATEGORIES = self.__factory.get_categories()
        self.__composer = None

    def fetch(
        self,
        category=CATEGORY_COVULN,
        paths=None,
        from_date=DEFAULT_DATETIME,
        to_date=DEFAULT_LAST_DATETIME,
        branches=None,
        latest_items=False,
    ):
        """Fetch commits and add code vulnerabilities information."""

        items = super().fetch(
            category,
            from_date=from_date,
            to_date=to_date,
            branches=branches,
            latest_items=latest_items,
        )

        self.__composer = self.__factory.get_composer(category)

        return items

    def _analyze(self, commit):
        """
        Analyse a commit and the corresponding
        checkout version of the repository.

        :param commit: a Perceval commit item
        :returns: a boolean value
        """

        if not self.__composer:
            raise GraalError(cause="running analyze without having set an analyzer")

        results = []

        analyzers = self.__composer.get_composition()
        for analyzer in analyzers:
            sub_analysis = analyzer.analyze(commit=commit, details=self.details,
                                            in_paths=self.in_paths, worktreepath=self.worktreepath)
            results.append(sub_analysis)

        merged_results = self.__composer.merge_results(results)

        return merged_results

    def _post(self, commit):
        """Remove attributes of the Graal item obtained

        :param commit: a Graal commit item
        """
        commit.pop("Author", None)
        commit.pop("Commit", None)
        commit.pop("files", None)
        commit.pop("parents", None)
        commit.pop("refs", None)

        commit['analyzer'] = self.__composer.get_kind()

        return commit

    @staticmethod
    def metadata_category(item):
        """Extracts the category from a Code item."""

        analyzer = item['analyzer']

        factory = CoVulnAnalyzerFactory()
        composer = factory.get_composer(analyzer)

        return composer.get_category()


class CoVulnCommand(GraalCommand):
    """Class to run CoVuln backend from the command line."""

    BACKEND = CoVuln
