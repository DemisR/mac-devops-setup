#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2015, James G. Kim <jgkim@jayg.org>
#
# Based on Homebrew Cask Ansible module (Daniel Jaouen <dcj24@cornell.edu>)
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: apm
author: "James G. Kim (@echo4ngel)"
short_description: Package manager for Atom
description:
    - Manages Atom packages
version_added: 1.9
options:
    name:
        description:
            - name of package to install/remove
        required: false
        default: None
    state:
        description:
            - state of the package
        choices: [ 'present', 'absent', 'latest' ]
        required: false
        default: present
    upgrade_all:
        description:
            - upgrade all Atom packages
        required: false
        default: no
        choices: [ "yes", "no" ]
notes: []
'''
EXAMPLES = '''
- apm: name=foo state=present
- apm: name=foo state=present upgrade_all=yes
- apm: upgrade_all=yes
- apm: name=foo state=absent
- apm: name=foo state=latest
- apm: name=foo,bar state=latest
'''

import os.path
import re


# exceptions -------------------------------------------------------------- {{{
class AtomException(Exception):
    pass
# /exceptions ------------------------------------------------------------- }}}


# utils ------------------------------------------------------------------- {{{
def _create_regex_group(s):
    lines = (line.strip() for line in s.split('\n') if line.strip())
    chars = filter(None, (line.split('#')[0].strip() for line in lines))
    group = r'[^' + r''.join(chars) + r']'
    return re.compile(group)
# /utils ------------------------------------------------------------------ }}}


class Atom(object):
    '''A class to manage Atom packages.'''

    # class regexes ------------------------------------------------ {{{
    VALID_PATH_CHARS = r'''
        \w                  # alphanumeric characters (i.e., [a-zA-Z0-9_])
        \s                  # spaces
        :                   # colons
        {sep}               # the OS-specific path separator
        .                   # dots
        -                   # dashes
    '''.format(sep=os.path.sep)

    VALID_APM_PATH_CHARS = r'''
        \w                  # alphanumeric characters (i.e., [a-zA-Z0-9_])
        \s                  # spaces
        {sep}               # the OS-specific path separator
        .                   # dots
        -                   # dashes
    '''.format(sep=os.path.sep)

    VALID_PACKAGE_CHARS = r'''
        \w                  # alphanumeric characters (i.e., [a-zA-Z0-9_])
        -                   # dashes
    '''

    INVALID_PATH_REGEX        = _create_regex_group(VALID_PATH_CHARS)
    INVALID_APM_PATH_REGEX    = _create_regex_group(VALID_APM_PATH_CHARS)
    INVALID_PACKAGE_REGEX     = _create_regex_group(VALID_PACKAGE_CHARS)
    # /class regexes ----------------------------------------------- }}}

    # class validations -------------------------------------------- {{{
    @classmethod
    def valid_path(cls, path):
        '''
        `path` must be one of:
         - list of paths
         - a string containing only:
             - alphanumeric characters
             - dashes
             - dots
             - spaces
             - colons
             - os.path.sep
        '''

        if isinstance(path, basestring):
            return not cls.INVALID_PATH_REGEX.search(path)

        try:
            iter(path)
        except TypeError:
            return False
        else:
            paths = path
            return all(cls.valid_apm_path(path_) for path_ in paths)

    @classmethod
    def valid_apm_path(cls, apm_path):
        '''
        `apm_path` must be one of:
         - None
         - a string containing only:
             - alphanumeric characters
             - dashes
             - dots
             - spaces
             - os.path.sep
        '''

        if apm_path is None:
            return True

        return (
            isinstance(apm_path, basestring)
            and not cls.INVALID_APM_PATH_REGEX.search(apm_path)
        )

    @classmethod
    def valid_package(cls, package):
        '''A valid package is either None or alphanumeric.'''

        if package is None:
            return True

        return (
            isinstance(package, basestring)
            and not cls.INVALID_PACKAGE_REGEX.search(package)
        )

    @classmethod
    def valid_state(cls, state):
        '''
        A valid state is one of:
            - None
            - installed
            - upgraded
            - absent
        '''

        if state is None:
            return True
        else:
            return (
                isinstance(state, basestring)
                and state.lower() in (
                    'installed',
                    'upgraded',
                    'absent',
                )
            )

    @classmethod
    def valid_module(cls, module):
        '''A valid module is an instance of AnsibleModule.'''

        return isinstance(module, AnsibleModule)

    # /class validations ------------------------------------------- }}}

    # class properties --------------------------------------------- {{{
    @property
    def module(self):
        return self._module

    @module.setter
    def module(self, module):
        if not self.valid_module(module):
            self._module = None
            self.failed = True
            self.message = 'Invalid module: {0}.'.format(module)
            raise AtomException(self.message)

        else:
            self._module = module
            return module

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        if not self.valid_path(path):
            self._path = []
            self.failed = True
            self.message = 'Invalid path: {0}.'.format(path)
            raise AtomException(self.message)

        else:
            if isinstance(path, basestring):
                self._path = path.split(':')
            else:
                self._path = path

            return path

    @property
    def apm_path(self):
        return self._apm_path

    @apm_path.setter
    def apm_path(self, apm_path):
        if not self.valid_apm_path(apm_path):
            self._apm_path = None
            self.failed = True
            self.message = 'Invalid apm_path: {0}.'.format(apm_path)
            raise AtomException(self.message)

        else:
            self._apm_path = apm_path
            return apm_path

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        self._params = self.module.params
        return self._params

    @property
    def current_package(self):
        return self._current_package

    @current_package.setter
    def current_package(self, package):
        if not self.valid_package(package):
            self._current_package = None
            self.failed = True
            self.message = 'Invalid package: {0}.'.format(package)
            raise AtomException(self.message)

        else:
            self._current_package = package
            return package
    # /class properties -------------------------------------------- }}}

    def __init__(self, module, path=None, packages=None, state=None,
                 upgrade_all=False):
        self._setup_status_vars()
        self._setup_instance_vars(module=module, path=path, packages=packages,
                                  state=state, upgrade_all=upgrade_all, )

        self._prep()

    # prep --------------------------------------------------------- {{{
    def _setup_status_vars(self):
        self.failed = False
        self.changed = False
        self.changed_count = 0
        self.unchanged_count = 0
        self.message = ''

    def _setup_instance_vars(self, **kwargs):
        for key, val in kwargs.iteritems():
            setattr(self, key, val)

    def _prep(self):
        self._prep_path()
        self._prep_apm_path()

    def _prep_path(self):
        if not self.path:
            self.path = ['/usr/local/bin']

    def _prep_apm_path(self):
        if not self.module:
            self.apm_path = None
            self.failed = True
            self.message = 'AnsibleModule not set.'
            raise AtomException(self.message)

        self.apm_path = self.module.get_bin_path(
            'apm',
            required=True,
            opt_dirs=self.path,
        )
        if not self.apm_path:
            self.apm_path = None
            self.failed = True
            self.message = 'Unable to locate Atom package manager (apm) executable.'
            raise AtomException('Unable to locate Atom package manager (apm) executable.')

        return self.apm_path

    def _status(self):
        return (self.failed, self.changed, self.message)
    # /prep -------------------------------------------------------- }}}

    def run(self):
        try:
            self._run()
        except AtomException:
            pass

        if not self.failed and (self.changed_count + self.unchanged_count > 1):
            self.message = "Changed: %d, Unchanged: %d" % (
                self.changed_count,
                self.unchanged_count,
            )
        (failed, changed, message) = self._status()

        return (failed, changed, message)

    # checks ------------------------------------------------------- {{{
    def _current_package_is_installed(self):
        if not self.valid_package(self.current_package):
            self.failed = True
            self.message = 'Invalid package: {0}.'.format(self.current_package)
            raise AtomException(self.message)

        cmd = [
            "{apm_path}".format(apm_path=self.apm_path),
            'list',
            '--bare',
            '--installed',
        ]
        rc, out, err = self.module.run_command(cmd)
        if rc == 0:
            pattern = r'^' + re.escape(self.current_package) + r'(?=@)'
            return bool(re.search(pattern, out, re.MULTILINE | re.IGNORECASE))
        else:
            self.failed = True
            self.message = err.strip()
            raise AtomException(self.message)

        return False

    def _current_package_is_outdated(self):
        if not self.valid_package(self.current_package):
            return False

        rc, out, err = self.module.run_command([
            self.apm_path,
            'outdated',
            self.current_package,
        ])

        if rc == 0:
            return bool(re.search(re.escape(self.current_package), out, re.MULTILINE | re.IGNORECASE))
        else:
            self.failed = True
            self.message = err.strip()
            raise AtomException(self.message)

        return False
    # /checks ------------------------------------------------------ }}}

    # commands ----------------------------------------------------- {{{
    def _run(self):
        if self.upgrade_all:
            self._upgrade_all()

        if self.packages:
            if self.state == 'installed':
                return self._install_packages()
            elif self.state == 'upgraded':
                return self._upgrade_packages()
            elif self.state == 'absent':
                return self._uninstall_packages()

    # _upgrade_all --------------------------- {{{
    def _upgrade_all(self):
        rc, out, err = self.module.run_command([
            self.apm_path,
            'upgrade',
            '--no-confirm',
        ])
        if rc == 0:
            if re.search(re.escape('(empty)'), out, re.MULTILINE | re.IGNORECASE):
                self.message = 'Atom packages already upgraded.'

            else:
                self.changed = True
                self.message = 'Atom upgraded.'

            return True
        else:
            self.failed = True
            self.message = err.strip()
            raise AtomException(self.message)
    # /_upgrade_all -------------------------- }}}

    # installed ------------------------------ {{{
    def _install_current_package(self):
        if not self.valid_package(self.current_package):
            self.failed = True
            self.message = 'Invalid package: {0}.'.format(self.current_package)
            raise AtomException(self.message)

        if self._current_package_is_installed():
            self.unchanged_count += 1
            self.message = 'Package already installed: {0}'.format(
                self.current_package,
            )
            return True

        if self.module.check_mode:
            self.changed = True
            self.message = 'Package would be installed: {0}'.format(
                self.current_package
            )
            raise AtomException(self.message)

        cmd = [opt
               for opt in (self.apm_path, 'install', self.current_package)
               if opt]

        rc, out, err = self.module.run_command(cmd)

        if self._current_package_is_installed():
            self.changed_count += 1
            self.changed = True
            self.message = 'Package installed: {0}'.format(self.current_package)
            return True
        else:
            self.failed = True
            self.message = err.strip()
            raise AtomException(self.message)

    def _install_packages(self):
        for package in self.packages:
            self.current_package = package
            self._install_current_package()

        return True
    # /installed ----------------------------- }}}

    # upgraded ------------------------------- {{{
    def _upgrade_current_package(self):
        command = ['upgrade', '--no-confirm']

        if not self.valid_package(self.current_package):
            self.failed = True
            self.message = 'Invalid package: {0}.'.format(self.current_package)
            raise AtomException(self.message)

        if not self._current_package_is_installed():
            command = 'install'

        if self._current_package_is_installed() and not self._current_package_is_outdated():
            self.message = 'Package is already upgraded: {0}'.format(
                self.current_package,
            )
            self.unchanged_count += 1
            return True

        if self.module.check_mode:
            self.changed = True
            self.message = 'Package would be upgraded: {0}'.format(
                self.current_package
            )
            raise AtomException(self.message)

        opts = (
            [self.apm_path]
            + command
            + [self.current_package]
        )
        cmd = [opt for opt in opts if opt]
        rc, out, err = self.module.run_command(cmd)

        if self._current_package_is_installed() and not self._current_package_is_outdated():
            self.changed_count += 1
            self.changed = True
            self.message = 'Package upgraded: {0}'.format(self.current_package)
            return True
        else:
            self.failed = True
            self.message = err.strip()
            raise AtomException(self.message)

    def _upgrade_packages(self):
        if not self.packages:
            self._upgrade_all()
        else:
            for package in self.packages:
                self.current_package = package
                self._upgrade_current_package()
            return True
    # /upgraded ------------------------------ }}}

    # uninstalled ---------------------------- {{{
    def _uninstall_current_package(self):
        if not self.valid_package(self.current_package):
            self.failed = True
            self.message = 'Invalid package: {0}.'.format(self.current_package)
            raise AtomException(self.message)

        if not self._current_package_is_installed():
            self.unchanged_count += 1
            self.message = 'Package already uninstalled: {0}'.format(
                self.current_package,
            )
            return True

        if self.module.check_mode:
            self.changed = True
            self.message = 'Package would be uninstalled: {0}'.format(
                self.current_package
            )
            raise AtomException(self.message)

        cmd = [opt
               for opt in (self.apm_path, 'uninstall', self.current_package)
               if opt]

        rc, out, err = self.module.run_command(cmd)

        if not self._current_package_is_installed():
            self.changed_count += 1
            self.changed = True
            self.message = 'Package uninstalled: {0}'.format(self.current_package)
            return True
        else:
            self.failed = True
            self.message = err.strip()
            raise AtomException(self.message)

    def _uninstall_packages(self):
        for package in self.packages:
            self.current_package = package
            self._uninstall_current_package()

        return True
    # /uninstalled ----------------------------- }}}
    # /commands ---------------------------------------------------- }}}


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(
                aliases=["pkg", "package"],
                required=False,
                type='list',
            ),
            path=dict(required=False),
            state=dict(
                default="present",
                choices=[
                    "present", "installed",
                    "absent", "removed", "uninstalled",
                    "latest", "upgraded",
                ],
            ),
            upgrade_all=dict(
                default=False,
                aliases=["upgrade"],
                type='bool',
            ),
        ),
        supports_check_mode=True,
    )
    p=module.params

    if p['name']:
        packages = p['name']
    else:
        packages = None

    path = p['path']
    if path:
        path = path.split(':')
    else:
        path = ['/usr/local/bin']

    state = p['state']
    if state in ('present', 'installed'):
        state = 'installed'
    if state in ('latest', 'upgraded'):
        state = 'upgraded'
    if state in ('absent', 'removed', 'uninstalled'):
        state = 'absent'

    upgrade_all = p['upgrade_all']

    apm = Atom(module=module, path=path, packages=packages,
               state=state, upgrade_all=upgrade_all)

    (failed, changed, message) = apm.run()
    if failed:
        module.fail_json(msg=message)
    else:
        module.exit_json(changed=changed, msg=message)

# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *

if __name__ == '__main__':
  main()
