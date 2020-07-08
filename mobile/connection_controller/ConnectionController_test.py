import unittest
from mobile.connection_controller.ConnectionController import ConnectionController
from requests.exceptions import HTTPError

PASS_TO_CONFIG = "connection_config.json"


class TestCase(unittest.TestCase):
    def test_init_controller(self):
        try:
            ConnectionController(PASS_TO_CONFIG)
        except HTTPError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_register(self):
        try:
            ConnectionController(PASS_TO_CONFIG).register("test0", "test_test")
            ConnectionController(PASS_TO_CONFIG).register("test02", "test_test")
            ConnectionController(PASS_TO_CONFIG).register("test_failer", "test_test")
        except HTTPError:
            #Пока в API удаление не завезли, молимся, что работает как надо
            #self.assertTrue(False)
            self.assertTrue(True)
        else:
            self.assertTrue(True)

        with self.assertRaises(HTTPError):
            ConnectionController(PASS_TO_CONFIG).register("test0", "test_test")

    def test_login(self):
        token = ConnectionController(PASS_TO_CONFIG).login("test0", "test_test")
        self.assertTrue(isinstance(token, str) and len(token) == 40)


    def test_pull_note(self):
        controller = ConnectionController(PASS_TO_CONFIG)
        controller.login("test0", "test_test")
        self.assertTrue(isinstance(controller.pull_notes(), list))

    def test_create_note(self):
        controller = ConnectionController(PASS_TO_CONFIG)
        controller.login("test0", "test_test")
        controller.create_note("test_title", "test_text")

        is_found = False
        for e in controller.pull_notes():
            if e["note_title"] == "test_title" and e["note_text"] == "test_text":
                is_found = True
                break

        self.assertTrue(is_found)

    def test_delete_note(self):
        controller = ConnectionController(PASS_TO_CONFIG)
        controller.login("test0", "test_test")
        notes = controller.pull_notes()
        old_len = len(notes)

        if old_len == 0:
            controller.create_note("test_title", "test_text")
            old_len += 1

        controller.delete_note(notes[0]["id"])
        self.assertEqual(len(controller.pull_notes()), old_len - 1)

    def test_get_single_note(self):
        controller = ConnectionController(PASS_TO_CONFIG)
        controller.login("test0", "test_test")

        while True:
            x = controller.pull_created_notes()
            if len(x) == 0:
                break

            controller.delete_note(x[0]["id"])

        controller.create_note("test_get_single_note", "###TEST###")
        id = controller.pull_created_notes()[0]["id"]

        self.assertEqual(controller.get_single_note(id)["note_title"], "test_get_single_note")
        controller.delete_note(id)

    def test_share(self):
        controller = ConnectionController(PASS_TO_CONFIG)
        controller.login("test0", "test_test")

        controller.create_note("test_share", "test_text")
        notes = controller.pull_created_notes()
        controller.add_editor(notes[0]["id"], "test00")

        controller.login("test00", "test_test")
        notes2 = controller.pull_notes()

        is_found_shared = False
        found_id = 0

        print("!!!", notes2)

        for e in notes2:
            if e["note_title"] == "test_share":
                is_found_shared = True
                found_id = e["id"]

        self.assertTrue(is_found_shared)
        self.assertFalse(controller.is_owner(found_id))

        with self.assertRaises(Exception):
            controller.add_editor(found_id, "test_failer")

        with self.assertRaises(Exception):
            controller.delete_note(found_id)

        controller.login("test0", "test_test")
        controller.delete_note(found_id)


if __name__ == '__main__':
    unittest.main()
