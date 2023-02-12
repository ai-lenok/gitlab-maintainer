#!/usr/bin/env python3
from gitlab.maintainer import GitLabMaintainer

if __name__ == '__main__':
    approver = GitLabMaintainer()
    approver.approve()
