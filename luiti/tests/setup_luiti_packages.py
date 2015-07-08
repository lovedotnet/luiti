# -*- coding: utf-8 -*-

__all__ = ['SetupLuitiPackages']

import os
import sys
from etl_utils import cached_property, singleton


@singleton()
class SetupLuitiPackagesClass(object):

    @cached_property
    def config(self):
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        assert os.path.exists(root_dir), root_dir

        parent = os.path.join(root_dir, "tests/webui_packages")

        from luiti import config

        luiti_package_names = "dump clean middle summary".split(" ")
        for project_name in luiti_package_names + ["webui_tests"]:
            package_path = os.path.join(parent, "luiti_" + project_name)
            sys.path.insert(0, package_path)

        # setup env
        config.curr_project_dir = os.path.join(root_dir, "tests/webui_packages/luiti_summary")

        return config

SetupLuitiPackages = SetupLuitiPackagesClass()