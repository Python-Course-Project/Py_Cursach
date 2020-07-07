import requests
from requests.compat import urljoin
import json

cfg_pass = "connection_config.json"


class ConnectionController:
    def __init__(self):
        with open(cfg_pass) as cfg:
            self.cfg = json.load(cfg)

        self.username = self.cfg["username"]
        self.token = self.cfg["auth_token"]
        self.url = self.cfg["base_path"]
        self.api_ver = "api/" + self.cfg["api_version"]

    def __del__(self):
        with open(cfg_pass, 'w', encoding='utf-8') as cfg:
            json.dump(self.cfg, cfg, ensure_ascii=False, indent=4)

    @classmethod
    def register(cls, login, password):
        self = cls()
        get_register_url = urljoin(self.url, self.api_ver+"/auth/users/")
        response = requests.get(get_register_url, data={'username': login, 'password': password})

        if not response.ok:
            response.raise_for_status()

        self.cfg["username"] = login

    @classmethod
    def login(cls, login, password):
        self = cls()
        get_register_url = urljoin(self.url, self.api_ver+"/auth_token/token/login")
        response = requests.post(get_register_url, data={'username': login, 'password': password})

        if not response.ok:
            response.raise_for_status()

        self.cfg["username"] = login
        self.cfg["auth_token"] = response.json()["auth_token"]

    #def create_note(self, title, text):





#ConnectionController.login("test1", "testtesttest")
