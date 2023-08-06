#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020 Pradyumna Paranjape
# This file is part of pspman.
#
# pspman is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pspman is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pspman.  If not, see <https://www.gnu.org/licenses/>.
#
'''
PSPMAN: PSeudo Package Manager

'''

# Globally defined environment configuration
from pathlib import Path

from psprint import init_print

from pspman.classes import InstallEnv
from pspman.config import read_config

# Type: PathLike To be fixed in psprint
print = init_print(Path(__file__).resolve().parent.joinpath(
    ".psprintrc.yml")).psprint  # type: ignore
'''
Customized psprint function

'''

# ConfigBase
CONFIG = read_config()
'''
Meta data information about C_DIR(s), configuration directory, etc
'''

# set configurations
ENV = InstallEnv(CONFIG)
'''
Standard installation context
'''

__version__ = '1!1.5.1'
