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
Define variables from command line and defaults

'''

import argparse
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Union

import argcomplete
import yaml
from psprint import print
from xdgpspconf import utils

from pspman import CONFIG
from pspman.classes import InstallEnv
from pspman.config import MetaConfig
from pspman.tools import timeout


def parse_install_yml(inyaml: Path = None) -> List[str]:
    """
    Parse input file to extract installation urls

    Args:
        inyaml: path to installation input file

    Returns:
        Extracted installation list
    """
    if inyaml is None:
        return []
    with open(inyaml) as install_h:
        _install_urls: Union[str, List[str],
                             Dict[str, str]] = yaml.safe_load(install_h)
    install_urls: List[str] = []
    for gitline in _install_urls:
        if isinstance(gitline, str):
            install_urls.append(gitline)
        elif isinstance(gitline, dict):
            install_urls.append(*gitline.values())
        elif isinstance(gitline, list):
            install_urls.append(*gitline)  # type: ignore
    return install_urls


def cli(config: MetaConfig = None) -> argparse.ArgumentParser:
    '''
    Parse command line arguments

    Args:
        config: configuration to be modified by command line inputs

    Returns:
        modified ``confing``

    '''
    config = config or CONFIG
    description = '''

    \033[1;91mNOTICE: This is only intended for "user" packages.
    CAUTION: DO NOT RUN THIS SCRIPT AS ROOT.
    CAUTION: If you still insist, I won't care.\033[m
    '''

    d_pref = config.data_dir
    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.RawTextHelpFormatter)

    # base arguments
    parser.add_argument('--init',
                        action='store_true',
                        help='Initialize PSPMan')
    parser.add_argument('--version',
                        action='store_true',
                        help='Display version and exit')
    parser.add_argument('-l',
                        '--list',
                        action='store_true',
                        dest='info',
                        help='display list of cloned repositories and exit')
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='display verbose output')
    parser.add_argument('-s',
                        '--stale',
                        action='store_true',
                        help='skip updates, let repositories remain stale')
    parser.add_argument('-o',
                        '--only-pull',
                        action='store_true',
                        dest='pull',
                        help='only pull, do not try to install')
    parser.add_argument('-f',
                        '--force-risk',
                        action='store_true',
                        dest='risk',
                        help='force working with root permissions [DANGEROUS]')
    parser.add_argument('-p',
                        '--prefix',
                        type=Path,
                        nargs='?',
                        metavar='PREF',
                        help=f'path for installation [default: {d_pref}]',
                        default=d_pref)
    parser.add_argument('-c',
                        '--clone-dir',
                        type=Path,
                        nargs='?',
                        default=None,
                        metavar='C_DIR',
                        help=f'''Clone git repos in C_DIR.
Please check if you want to add this to PATH.
[default: PREF{os.sep}src]
''')
    parser.add_argument('-r',
                        '--reset',
                        metavar='PROJ',
                        type=str,
                        nargs='*',
                        default=[],
                        help='clean-reset PROJ code')
    parser.add_argument('-d',
                        '--delete',
                        metavar='PROJ',
                        type=str,
                        nargs='*',
                        default=[],
                        help='delete PROJ')
    parser.add_argument('-I',
                        '--install-from',
                        metavar='YML',
                        type=Path,
                        nargs='?',
                        default=None,
                        dest='inyaml',
                        help='Install packages from a yaml file')
    parser.add_argument('-i',
                        '--install',
                        metavar='URL',
                        type=str,
                        nargs='*',
                        default=[],
                        help=f'''
format: "URL[___branch[___'only'|___inst_argv[___sh_env]]]"

* *REMEMBER QUOTATION MARKS*

* URL: url to be cloned.
* branch: custom branch to clone. Blank implies default.
* pull_only: 'true', 'only', 'pull', 'hold' => Don't try to install this URL
* inst_argv: Custom arguments. These are passed *raw* during installation.
* sh_env: VAR1=VAL1,VAR2=VAL2,VAR3=VAL3.... Modified install environment.

''')
    parser.set_defaults(call_function=None)

    # sub-commands
    sub_parsers = parser.add_subparsers()

    version = sub_parsers.add_parser(name='version',
                                     aliases=['ver'],
                                     help='display version and exit')
    version.set_defaults(call_function='version')

    switch = sub_parsers.add_parser(
        name='switch',
        aliases=['activate', 'export'],
        help='switch to environment temporarily\n' +
        'with additional *PATH variables from PREFIX')
    switch.add_argument('switch_to',
                        type=str,
                        metavar='GIT_GROUP|PATH',
                        help="GIT_GROUP's name or path",
                        nargs='?',
                        default='default')
    switch.add_argument('-c',
                        '--copy',
                        action='store_true',
                        dest='clipboard',
                        help='try to copy soruce command to clipboard')
    switch.set_defaults(call_function='switch')

    unlock = sub_parsers.add_parser(name='unlock',
                                    aliases=[],
                                    help='Unlock C_DIR and exit')
    unlock.set_defaults(call_function='unlock')

    list_gits = sub_parsers.add_parser(
        name='list',
        aliases=['info'],
        help='display list of cloned repositories and exit')
    list_gits.add_argument('--meta',
                           '-m',
                           action='store_true',
                           help='List known C_DIR(s)')
    list_gits.set_defaults(call_function='info')

    init = sub_parsers.add_parser(name='init',
                                  aliases=['initialize'],
                                  help='initialize pspman')
    init.add_argument('--ignore',
                      '-i',
                      type=str,
                      metavar='DEP',
                      nargs='*',
                      help='initialize without dependency DEP')
    init.set_defaults(call_function='init')

    goodbye = sub_parsers.add_parser(name='goodbye',
                                     aliases=['de-initialize'],
                                     help='Cleanup before uninstalling pspman')
    goodbye.set_defaults(call_function='goodbye')

    return parser


def cli_opts(config: MetaConfig = None) -> Dict[str, Any]:
    '''
    Parse cli arguments to return its dict
    '''
    config = config or CONFIG
    parser = cli()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.info:
        setattr(args, 'call_function', 'info')
    if hasattr(args, 'meta'):
        if args.meta:
            setattr(args, 'call_function', 'meta')
        else:
            setattr(args, 'call_function', 'info')
    if args.version:
        setattr(args, 'call_function', 'version')
    if args.init:
        setattr(args, 'call_function', 'init')
    cli_args = vars(args)
    cli_args['install'].extend(parse_install_yml(cli_args['inyaml']))
    return cli_args


def perm_pass(env: InstallEnv, permdir: Path) -> int:
    '''
    Args:
        permdir: directory whose permissions are to be checked

    Returns:
        Error code: ``1`` if all rwx permissions are not granted

    '''
    if env.verbose:
        print(f'Checking permissions for {permdir}')
    user = os.environ.get('USER', 'root')
    access = utils.fs_perm(path=permdir, mode='rwx')
    if access:
        return 0
    print(f'We [{user}] do not have sufficient permissions on {permdir}',
          mark=5)
    print('Try another location', mark=2)
    return 1


def prepare_env(env: InstallEnv) -> int:
    '''
    Check permissions and create prefix and source directories

    Returns:
        Error code
    '''
    # Am I root?
    if os.environ.get('USER', 'root').lower() == 'root':
        print('I hate dictators', mark=3)
        if not env.risk:
            print('Bye', mark=0)
            return 2
        print('I can only hope you know what you are doing...', mark=3)
        print('Here is a chance to kill me in', mark=2)
        try:
            timeout(10)
        except:
            print("Aborting.", pref_color='g', pref=chr(0x1f197), short=False)
            return 1
        print()
        print("Your decision",
              pref=chr(0x1f937),
              pref_color='r',
              text_color="y",
              short=False)
        print()
        print('Proceeding...', mark=1)
    else:
        # Is installation directory read/writable
        err = perm_pass(env=env, permdir=env.clone_dir)
        err += perm_pass(env=env, permdir=env.prefix)
        if err != 0:
            print('Bye', mark=0)
            return err
    env.clone_dir.mkdir(parents=True, exist_ok=True)
    env.prefix.mkdir(parents=True, exist_ok=True)
    return 0


def lock(env: InstallEnv, unlock: bool = False, message: str = None):
    '''
    Unlock up the directory

    Args:
        env: installation context
        unlock: unlock existing locks?
        message: message to be written in the lockfile instead of pid

    Returns:
        Error code

    '''
    lock_path = env.prefix.joinpath('.proc.lock')
    # lockfile is deliberately human-readable

    if lock_path.exists():
        # directory is locked
        if unlock:
            # restore all backup databases
            for filetype in "healthy", "fail":
                backup_file = env.clone_dir.joinpath(f".pspman.{filetype}.yml")
                if backup_file.with_suffix('.yml.bak').is_file() and \
                   not backup_file.is_file():
                    backup_file.with_suffix(".yml.bak").replace(backup_file)
            temp_build = env.prefix.joinpath('temp_build')
            if temp_build.is_dir():
                shutil.rmtree(temp_build)
            lock_path.unlink()
            return 1
        with open(lock_path, 'r') as lock_fh:
            print(f"This git-group was locked for safety by {lock_fh.read()}",
                  mark='err')
        print("Either wait for the process to get completed")
        print("OR interrupt the process and execute")
        print(f"pspman -p {env.prefix} unlock", mark='act')
        print("Interruption WILL generally MESS UP source codes.", mark='warn')
        return 2
    if unlock:
        print(f'Lockfile {lock_path} not found.')
        return 2
    with open(lock_path, 'w') as lock_fh:
        lock_fh.write(str(message) or 'pid:' + str(os.getpid()))
    return 0
