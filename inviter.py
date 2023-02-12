#!/usr/bin/env python3
from dynaconf import settings
from gitlab.maintainer import GitLabMaintainer

if __name__ == '__main__':
    for user in settings["users"]:
        inviter = GitLabMaintainer()
        repo_id = inviter.create_repo(user["name"], user["email"])
        inviter.unprotected_branch(repo_id, "main")
        inviter.protected_branch(repo_id, "main", settings["access_level"])
        inviter.protected_branch(repo_id, "review", 40)
        inviter.invite(repo_id, user["email"])
