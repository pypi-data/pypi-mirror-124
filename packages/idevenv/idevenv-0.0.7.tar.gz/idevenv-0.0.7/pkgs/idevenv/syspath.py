# -*- coding: utf-8 -*-
import os
import sys
from platform import python_version_tuple
from pathlib import PureWindowsPath, PurePosixPath

from idevenv._utils import *


__all__ = [
    'Syspath',
    'clean_path',
]


def clean_path(p):
    # 운영체제 타입에 따라 path 를 수정한다
    if os.name == 'posix':
        return str(PurePosixPath(p))
    elif os.name == 'nt':
        return str(PureWindowsPath(p))



class Syspath(object):
    # pip로 설치되지 않은 패키지들의 경로를 수동으로 추가한다
    # 그러나, 최종적으로는 pip를 사용하라

    def __init__(self, projectName, basepath='C:/pypjts', package_dir='pkgs'):
        self.set_BasePath(basepath)
        self.ProjectName = projectName
        self._package_dir = package_dir
        self.ProjectPath = clean_path(f'{self.BasePath}/{self.ProjectName}')
        self.add_project_packages()

    def set_BasePath(self, p):
        if p is None:
            if os.name == 'posix':
                p = '/Users/sambong/pypjts'
            elif os.name == 'nt':
                p = 'C:/pypjts'
        else:
            p = clean_path(p)
        self._basepath = clean_path(p)

    @property
    def BasePath(self):
        return self._basepath

    def view(self):
        pretty_title(f'Current sys.path at {__file__}')
        pp.pprint(sorted(set(sys.path)))

    def add_venv_site_packages(self, dirname='env'):
        # VirtualEnv Site-Packages 경로를 추가한다
        if os.name == 'posix':
            v = python_version_tuple()
            envpath = f"{dirname}/lib/python{v[0]}.{v[1]}/site-packages"
        elif os.name == 'nt':
            envpath = f"{dirname}/Lib/site-packages"
        p = clean_path(f"{self.ProjectPath}/{envpath}")
        sys.path.append(p)
        sys.path = sorted(set(sys.path))

    def add_project_packages(self):
        # 소스코드 패키지 경로를 추가한다
        p = clean_path(f"{self.ProjectPath}/{self._package_dir}")
        sys.path.append(p)
        sys.path = sorted(set(sys.path))

    def add_uninstall_packages(self, projects, package_dir=None):
        self._package_dir = self._package_dir if package_dir is None else package_dir
        uninstalls = []
        for project in projects:
            p = clean_path(f"{self._basepath}/{project}/{self._package_dir}")
            sys.path.append(p)
            uninstalls.append(p)
        sys.path = sorted(set(sys.path))

        pretty_title(f'!!! 경고 !!! at {__file__}')
        print('임시로 추가한 패키지들 경로:')
        pp.pprint(sorted(uninstalls))
