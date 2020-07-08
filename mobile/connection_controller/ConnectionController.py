import requests
from requests.compat import urljoin
import json


class ConnectionController:
    def __init__(self, config_pwd="connection_config.json"):
        self.cfg_pwd = "connection_config.json"
        with open(config_pwd) as cfg:
            self.cfg = json.load(cfg)

        self.username = self.cfg["username"]
        self.token = self.cfg["auth_token"]
        self.url = self.cfg["base_path"]
        self.api_ver = "api/" + self.cfg["api_version"]

    def __del__(self):
        with open(self.cfg_pwd, 'w', encoding='utf-8') as cfg:
            json.dump(self.cfg, cfg, ensure_ascii=False, indent=4)

    @classmethod
    def register(cls, login, password):
        self = cls()
        print(self.cfg)
        get_register_url = urljoin(self.url, self.api_ver + "/auth/users/")
        response = requests.post(get_register_url, data={'username': login, 'password': password})

        if not response.ok:
            response.raise_for_status()

        self.cfg["username"] = login

    @classmethod
    def login(cls, login, password):
        self = cls()
        get_register_url = urljoin(self.url, self.api_ver + "/auth_token/token/login")
        response = requests.post(get_register_url, data={'username': login, 'password': password})

        if not response.ok:
            response.raise_for_status()

        self.cfg["username"] = login
        self.cfg["auth_token"] = response.json()["auth_token"]

        return self.cfg["auth_token"]

    @classmethod
    def create_note(cls, title, text):
        self = cls()
        response = requests.post('https://nameless-sands-73623.herokuapp.com/api/v1/note/create/',
                                 data={"note_title": title, "note_text": text},
                                 headers={"Authorization": "Token " + self.token})

        if not response.ok:
            response.raise_for_status()

    @classmethod
    def pull_notes(cls):
        self = cls()
        response_editor = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/note/all/as_editor/",
                                       headers={"Authorization": "Token " + self.token})

        response_json = response_editor.json() + self.pull_created_notes()

        return response_json

    @classmethod
    def pull_created_notes(cls):
        self = cls()
        response_creator = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/note/all/as_creator/",
                                        headers={"Authorization": "Token " + self.token})

        return response_creator.json()

    @classmethod
    def is_owner(cls, note_id):
        for note in cls.pull_created_notes():
            if note["id"] == note_id:
                return True

        return False

    @classmethod
    def get_single_note(cls, note_id):
        self = cls()
        url = "https://nameless-sands-73623.herokuapp.com/api/v1/note/detail/" + str(note_id) + "/creator"
        prev = requests.get(url, headers={"Authorization": "Token " + self.token})

        if not prev.ok:
            prev.raise_for_status()

        return prev.json()

    @classmethod
    def delete_note(cls, note_id):
        self = cls()
        if cls.is_owner(note_id):
            url = "https://nameless-sands-73623.herokuapp.com/api/v1/note/detail/" + str(note_id) + "/creator"
            response = requests.delete(url, headers={"Authorization": "Token " + self.token})
            if not response.ok:
                response.raise_for_status()

        else:
            raise Exception("Unauthorized delete request with note_id:{} by user:{}".format(note_id, self.username))

    @classmethod
    def patch_note(cls, note_id: int, new_text: str):
        note = cls.get_single_note(note_id)
        note["note_text"] = new_text

        url = "https://nameless-sands-73623.herokuapp.com/api/v1/note/detail/" + str(note_id) + "/creator"
        r = requests.patch(url, data=note, headers={"Authorization": "Token " + cls().token})

        if not r.ok:
            r.raise_for_status()

    @classmethod
    def rename_note(cls, note_id: int, new_title: str):
        self = cls()
        if not self.is_owner(note_id):
            raise Exception("Rename request by not-creator with note_id:{} by user:{}".format(note_id, self.username))

        url = "https://nameless-sands-73623.herokuapp.com/api/v1/note/detail/" + str(note_id) + "/creator"
        prev = requests.get(url, headers={"Authorization": "Token " + self.token})

        if not prev.ok:
            prev.raise_for_status()

        note = prev.json()
        note["note_title"] = new_title
        r = requests.patch(url, data=note, headers={"Authorization": "Token " + self.token})

        if not r.ok:
            r.raise_for_status()

    @classmethod
    def get_id(cls, name=None):
        self = cls()
        if name is None:
            name = self.username

        all_users = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/users/all/",
                             headers={"Authorization": "Token " + self.token})

        for e in all_users.json():
            if e["username"] == name:
                return e["id"]

    @classmethod
    def add_editor(cls, note_id: int, new_editor_username: str):
        self = cls()
        if not cls.is_owner(note_id):
            raise Exception("Unauthorized share for note_id:{} by user:{} to user:{}".format(note_id, self.username,
                                                                                             new_editor_username))

        note = cls.get_single_note(note_id)
        note["editor"].append(cls.get_id(new_editor_username))

        url = "https://nameless-sands-73623.herokuapp.com/api/v1/note/detail/" + str(note_id) + "/creator"
        r = requests.patch(url, data=note, headers={"Authorization": "Token " + cls().token})
        print(r.json())

        if not r.ok:
            r.raise_for_status()

#x = ConnectionController.login("test000", "test_test")
#print(x)