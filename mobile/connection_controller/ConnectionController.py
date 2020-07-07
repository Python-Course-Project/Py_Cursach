import requests
from requests.compat import urljoin
import json

cfg_pass = "connection_config.json"


class ConnectionController:
    def __init__(self, config_pwd=cfg_pass):
        with open(config_pwd) as cfg:
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
        get_register_url = urljoin(self.url, self.api_ver + "/auth/users/")
        response = requests.get(get_register_url, data={'username': login, 'password': password})

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
        response_creator = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/note/all/as_creator/",
                                        headers={"Authorization": "Token " + self.token})

        response_editor = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/note/all/as_editor/",
                                       headers={"Authorization": "Token " + self.token})

        response_json = response_editor.json() + response_creator.json()

        return response_json

    @classmethod
    def is_owner(cls, note_id):
        self = cls()
        response_creator = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/note/all/as_creator/",
                                        headers={"Authorization": "Token " + self.token})
        for note in response_creator.json():
            if note["id"] == note_id:
                return True

        return False

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
        self = cls()
        url = "https://nameless-sands-73623.herokuapp.com/api/v1/note/detail/" + str(note_id) + "/creator"
        prev = requests.get(url, headers={"Authorization": "Token " + self.token})

        if not prev.ok:
            prev.raise_for_status()

        note = prev.json()
        note["note_text"] = new_text
        r = requests.patch(url, data=note, headers={"Authorization": "Token " + self.token})

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

    # @classmethod
    # def patch_note(cls, note_id: int, new_text: str):
    #     self = cls()
    #     url = "https://nameless-sands-73623.herokuapp.com/api/v1/note/detail/" + str(note_id) + "/creator"
    #     prev = requests.get(url, headers={"Authorization": "Token " + self.token})
    #
    #     if not prev.ok:
    #         prev.raise_for_status()
    #
    #     note = prev.json()
    #     note["note_text"] = new_text
    #     r = requests.patch(url, data=note, headers={"Authorization": "Token " + self.token})
    #
    #     if not r.ok:
    #         r.raise_for_status()



ConnectionController.login("test2", "testtesttest")
#ConnectionController.create_note("Hi", "Benny")
x = ConnectionController.pull_notes()
print(x)


#ConnectionController.patch_note(x[0]["id"], "Ананас")
x = ConnectionController.pull_notes()
print(x)

#ConnectionController.login("test1", "testtesttest")
#x = ConnectionController.pull_notes()
#print(x)
# ConnectionController.rename_note(32, "WAAAT")
# print(ConnectionController.pull_notes())
# # ConnectionController.create_note("Oh", "Hi Mark")
# # print(ConnectionController.is_owner(20))
# # print(ConnectionController.is_owner(30))
# ConnectionController.delete_note(30)
# print(ConnectionController.pull_notes())
# ConnectionController.delete_note(95)
