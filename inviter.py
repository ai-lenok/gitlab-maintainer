#!/usr/bin/env python3
import requests
import re
import logging
from dynaconf import settings


class Inviter:
    def __init__(self, name: str, email: str):
        logging.basicConfig(level=settings["log_level"],
                            format=settings["log_format"])
        self.logger = logging.getLogger('Inviter')

        self.host_projects = f'{settings["host"]}/api/v4/projects'
        self.header = {"Authorization": f'Bearer {settings["auth_token"]}'}
        self.id = 0

        self.name = name
        self.email = email

        self.template_url = settings["template_url"]
        self.expires_invite = settings["expires_invite"]
        self.access_level = settings["access_level"]
        self.maintainer_level = 40
        self.namespace_id = settings["namespace_id"]

        self.logger.info(f'Invite user "{self.name}" "{self.email}"')
        self.logger.debug(self.host_projects)

    def show_all(self):
        res = requests.get(self.host_projects, headers=self.header)
        self.logger.info(res.json())

    def show(self, id: int):
        res = requests.get(f"{self.host_projects}/{id}", headers=self.header)
        self.logger.info(res.json())

    def create_repo(self):
        path_email = re.sub(r"[@.]", "-", self.email)
        self.logger.info(f"Create repo: {path_email}")
        data = {
            "name": f"{self.name}",
            "path": f"{path_email}",
            "description": f"{self.name}: Решение олимпиадной задачи",
            "namespace_id": self.namespace_id,
            "import_url": self.template_url
        }
        res = requests.post(self.host_projects, data, headers=self.header)
        self.logger.info(res.json())
        self.id = res.json()["id"]
        return self.id

    def protected_branch(self):
        self.logger.info(f"Protected branch: {self.id}")
        self.logger.info(f"Unprotected branch main: {self.id}")
        res_delete = requests.delete(f"{self.host_projects}/{self.id}/protected_branches/main", headers=self.header)
        self.logger.info(res_delete)

        data = {
            "name": "main",
            "push_access_level": self.access_level,
            "merge_access_level": self.access_level,
            "unprotect_access_level": self.maintainer_level,
            "allow_force_push": False
        }
        self.logger.info(f"Protected branch main: {self.id}")
        res = requests.post(f"{self.host_projects}/{self.id}/protected_branches", data, headers=self.header)
        self.logger.info(res.json())

        data = {
            "name": "review",
            "push_access_level": self.maintainer_level,
            "merge_access_level": self.maintainer_level,
            "unprotect_access_level": self.maintainer_level,
            "allow_force_push": False
        }
        self.logger.info(f"Protected branch review: {self.id}")
        res = requests.post(f"{self.host_projects}/{self.id}/protected_branches", data, headers=self.header)
        self.logger.info(res.json())

    def invite(self):
        self.logger.info(f"Invite: {self.id} to {self.email}")
        data = {
            "email": self.email,
            "access_level": self.access_level,
            "expires_at": self.expires_invite
        }
        res = requests.post(f"{self.host_projects}/{self.id}/invitations", data, headers=self.header)
        self.logger.info(res.json())


if __name__ == '__main__':
    for user in settings["users"]:
        inviter = Inviter(user["name"], user["email"])
        inviter.create_repo()
        inviter.protected_branch()
        inviter.invite()
