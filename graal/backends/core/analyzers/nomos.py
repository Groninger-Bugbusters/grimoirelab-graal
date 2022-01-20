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

import os
import re
import subprocess

from graal.graal import (GraalError,
                         GraalRepository)
from .analyzer import Analyzer, is_in_paths


class Nomos(Analyzer):
    """A wrapper for Nomos.

    This class allows to call Nomos over a file, parses
    the result of the analysis and returns it as a dict.

    :param exec_path: path of the executable
    """
    version = '0.2.0'

    def __init__(self):
        self.search_pattern = re.compile(r'license\(s\) .*$')

    def analyze(self, **kwargs):
        """
        Add information about license

        :param file_path: file path

        :returns result: dict of the results of the analysis
        """

        exec_path = kwargs['exec_path']

        if not GraalRepository.exists(exec_path):
            raise GraalError(cause="executable path %s not valid" % exec_path)

        analysis = []
        license_info = {'licenses': []}

        for committed_file in kwargs['commit']['files']:
            file_path = committed_file['file']
            local_path = kwargs['worktreepath'] + '/' + file_path

            if not is_in_paths(kwargs['in_paths'], file_path):
                continue

            if not GraalRepository.exists(local_path) or os.path.isdir(local_path) or os.path.islink(local_path):
                continue

            try:
                msg = subprocess.check_output([exec_path, local_path]).decode("utf-8")
            except subprocess.CalledProcessError as e:
                raise GraalError(cause="Nomos failed at %s, %s" % (file_path, e.output.decode("utf-8")))
            finally:
                subprocess._cleanup()

            licenses_raw = re.findall(self.search_pattern, msg)

            licenses = []
            for license_raw in licenses_raw:
                license_digested = license_raw.split("license(s)")[1].strip()
                licenses.append(license_digested)

            if licenses:
                license_info['licenses'] = licenses

            license_info.update({'file_path': file_path})
            analysis.append(license_info)

        return analysis
