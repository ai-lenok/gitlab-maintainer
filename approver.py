#!/usr/bin/env python3
import requests
import logging
from dynaconf import settings


class Approver:
    def __init__(self):
        logging.basicConfig(level=settings["log_level"],
                            format=settings["log_format"])
        self.logger = logging.getLogger('Approver')
        self.host_users = f'{settings["host"]}/api/v4/users'
        self.header = {"Authorization": f'Bearer {settings["auth_token"]}'}
        self.users = {}

        for u in settings["users"]:
            self.users[u["email"]] = u["name"]

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
        for id in ids:
            self.logger.info(f"Approve {id}")
            res = requests.post(f"{self.host_users}/{id}/approve", headers=self.header)
            self.logger.info(res.json())


if __name__ == '__main__':
    approver = Approver()
    approver.approve()
