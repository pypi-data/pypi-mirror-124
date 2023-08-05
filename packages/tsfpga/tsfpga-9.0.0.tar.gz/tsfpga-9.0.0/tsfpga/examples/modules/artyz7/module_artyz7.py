# --------------------------------------------------------------------------------------------------
# Copyright (c) Lukas Vik. All rights reserved.
#
# This file is part of the tsfpga project.
# https://tsfpga.com
# https://gitlab.com/tsfpga/tsfpga
# --------------------------------------------------------------------------------------------------

from pathlib import Path

from tsfpga.constraint import Constraint
from tsfpga.module import BaseModule, get_tsfpga_modules
from tsfpga.examples.example_env import get_tsfpga_example_modules
from tsfpga.vivado.project import VivadoProject


THIS_FILE = Path(__file__)


class Module(BaseModule):
    def get_build_projects(self):
        projects = []

        modules = get_tsfpga_modules() + get_tsfpga_example_modules()
        part = "xc7z020clg400-1"

        tcl_dir = self.path / "tcl"
        pinning = Constraint(tcl_dir / "artyz7_pinning.tcl")
        block_design = tcl_dir / "block_design.tcl"

        projects.append(
            VivadoProject(
                name="artyz7",
                modules=modules,
                part=part,
                tcl_sources=[block_design],
                constraints=[pinning],
                defined_at=THIS_FILE,
            )
        )

        projects.append(
            SpecialVivadoProject(
                name="artyz7_dummy",
                modules=modules,
                part=part,
                top="artyz7_top",
                generics=dict(dummy=True, value=123),
                constraints=[pinning],
                tcl_sources=[block_design],
            )
        )

        return projects


class SpecialVivadoProject(VivadoProject):
    def post_build(self, output_path, **kwargs):  # pylint: disable=arguments-differ
        print(f"We can do useful things here. In the output path {output_path} for example")
        return True
