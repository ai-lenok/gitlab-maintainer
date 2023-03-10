from dynaconf import settings
from gitlab.maintainer import GitLabMaintainer

if __name__ == '__main__':
    maintainer = GitLabMaintainer()
    for repo_id in range(settings["start_repo_id"], settings["end_repo_id"] + 1):
        maintainer.unprotected_branch(repo_id, "main")
        maintainer.protected_branch(repo_id, "main", 40)