# Copyright FuseSoC contributors
# Licensed under the 2-Clause BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-2-Clause

import logging
import os.path
import shutil
import subprocess

from fusesoc.provider.provider import Provider
from fusesoc.utils import Launcher

logger = logging.getLogger(__name__)


class Git(Provider):
    @staticmethod
    def init_library(library):
        logger.info("Cloning library into {}".format(library.location))
        git_args = ["clone", library.sync_uri, library.location]

        if library.sync_branch:
            git_args.extend(["-b", library.sync_branch])

        Git._exec(git_args)

    @staticmethod
    def update_library(library):
        if not os.path.exists(library.location + "/.git"):
            Git.init_library(library)
        else:
            git_args = ["-C", library.location, "pull"]
            Git._exec(git_args)


    @staticmethod
    def _exec(git_args):
        try:
            Launcher("git", git_args).run()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(str(e))

    def _checkout(self, local_dir):
        version = self.config.get("version", None)

        # TODO : Sanitize URL
        repo = self.config.get("repo")
        logger.info("Checking out " + repo + " to " + local_dir)
        args = ["clone", "-q", repo, local_dir]
        Launcher("git", args).run()
        if version:
            args = ["-C", local_dir, "checkout", "-q", version]
            Launcher("git", args).run()
