"""sc-githooks - Checks on Git commits

Copyright (c) 2021 Scott Lau
Portions Copyright (c) 2021 InnoGames GmbH
Portions Copyright (c) 2021 Emre Hasegeli
"""

from githooks.config import config
from githooks.base_check import BaseCheck, Severity
from githooks.git import Commit


class CommitCheck(BaseCheck):
    """Parent class for all single commit checks"""
    commit = None

    def prepare(self, obj):
        new = super(CommitCheck, self).prepare(obj)
        if not new or not isinstance(obj, Commit):
            return new

        new = new.clone()
        new.commit = obj
        return new

    def __str__(self):
        return '{} 位于提交 {}'.format(type(self).__name__, self.commit)


class CheckChangedFilePaths(CommitCheck):
    """Check file names and directories on a single commit"""

    def get_problems(self):
        for changed_file in self.commit.get_changed_files():
            extension = changed_file.get_extension()
            if (
                    extension in ('pp', 'py', 'sh') and
                    changed_file.path != changed_file.path.lower()
            ):
                yield Severity.WARNING, '{} 文件名使用了大写字母'.format(changed_file)


class CheckBinaryFiles(CommitCheck):
    """Check whether binary files exists on a single commit"""

    def get_problems(self):
        # project_name = self.commit.get_projects()
        # projects_name = config.get("commit_check.unrestricted_projects")
        # projects = projects_name.split(",")
        # if project_name not in projects:
        for binary_file in self.commit.get_binary_files():
            yield Severity.WARNING, '文件 {} 是二进制文件'.format(binary_file)
