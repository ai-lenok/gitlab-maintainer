#!/usr/bin/env python3
import re
from dynaconf import settings
from gitlab.maintainer import GitLabMaintainer

if __name__ == '__main__':
    for user in settings["users"]:
        inviter = GitLabMaintainer()

        repo_path_from_email = re.sub(r"[@.]", "-", user["email"])
        repo_id = inviter.create_repo(user["name"], repo_path_from_email)

        inviter.unprotected_branch(repo_id, "main")
        inviter.protected_branch(repo_id, "main", settings["access_level"])
        inviter.protected_branch(repo_id, "review", 40)

        inviter.invite(repo_id, user["email"])
