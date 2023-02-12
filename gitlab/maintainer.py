import requests
import re
import logging
from dynaconf import settings


class GitLabMaintainer:
    def __init__(self):
        logging.basicConfig(level=settings["log_level"],
                            format=settings["log_format"])
        self.logger = logging.getLogger('GitLabMaintainer')
        self.host = settings["host"]
        self.host_projects = f'{settings["host"]}/api/v4/projects'
        self.host_users = f'{settings["host"]}/api/v4/users'
        self.header = {"Authorization": f'Bearer {settings["auth_token"]}'}

        self.template_url = settings["template_url"]
        self.expires_invite = settings["expires_invite"]
        self.access_level = settings["access_level"]
        self.maintainer_level = 40
        self.namespace_id = settings["namespace_id"]
        self.postfix_repo_name = settings["postfix_repo_name"]

        self.users = {}
        for u in settings["users"]:
            self.users[u["email"]] = u["name"]

        self.logger.info(f'GitLab host: {self.host}')

    def show_all(self):
        res = requests.get(self.host_projects, headers=self.header)
        self.logger.info(res.json())

    def show(self, repo_id: int):
        res = requests.get(f"{self.host_projects}/{repo_id}", headers=self.header)
        self.logger.info(res.json())

    def create_repo(self, repo_name: str, repo_path: str):
        self.logger.info(f"Create repo: {repo_path}")
        data = {
            "name": f"{repo_name}",
            "path": f"{repo_path}",
            "description": f"{repo_name}{self.postfix_repo_name}",
            "namespace_id": self.namespace_id,
            "import_url": self.template_url
        }
        res = requests.post(self.host_projects, data, headers=self.header)
        self.logger.info(res.json())
        return res.json()["id"]

    def unprotected_branch(self, repo_id: int, branch: str):
        self.logger.info(f"Unprotected branch main: {repo_id}")
        res_delete = requests.delete(f"{self.host_projects}/{repo_id}/protected_branches/{branch}", headers=self.header)
        self.logger.info(res_delete)

    def protected_branch(self, repo_id: int, branch: str, access_level=40):
        self.logger.info(f"Protected branch: {repo_id}")
        data = {
            "name": branch,
            "push_access_level": access_level,
            "merge_access_level": access_level,
            "unprotect_access_level": self.maintainer_level,
            "allow_force_push": False
        }
        self.logger.info(f"Protected branch main: {repo_id}")
        res = requests.post(f"{self.host_projects}/{repo_id}/protected_branches", data, headers=self.header)
        self.logger.info(res.json())

    def invite(self, repo_id: int, email: str):
        self.logger.info(f"Invite: {repo_id} to {email}")
        data = {
            "email": email,
            "access_level": self.access_level,
            "expires_at": self.expires_invite
        }
        res = requests.post(f"{self.host_projects}/{repo_id}/invitations", data, headers=self.header)
        self.logger.info(res.json())

    def get_all_users(self):
        res = requests.get(self.host_users, headers=self.header)
        return res.json()

    def find_unapproved_user(self):
        users = self.get_all_users()
        need_approves = []
        for u in users:
            if u["state"] == "blocked_pending_approval":
                user_name = f'User {u["id"]} {u["email"]} {u["username"]}'
                if u["email"] in self.users:
                    self.logger.info(f'{user_name} in white list. Add it.')
                    need_approves.append(u["id"])
                else:
                    self.logger.warning(f'{user_name} not in white list. Skip it.')
        return need_approves

    def approve(self):
        ids = self.find_unapproved_user()
        for user_id in ids:
            self.logger.info(f"Approve {user_id}")
            res = requests.post(f"{self.host_users}/{user_id}/approve", headers=self.header)
            self.logger.info(res.json())
