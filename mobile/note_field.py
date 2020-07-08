import json

from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.list import TwoLineListItem
from singleton_decorator import singleton

from mobile.connection_controller.ConnectionController import ConnectionController


@singleton
class NoteField(ScreenManager):
    note_list = ObjectProperty()

    redacted_text = ObjectProperty()
    redacted_title = ObjectProperty()

    button_data = {
        "pencil": "Edit note",
        "plus": "Create note",
        "cloud-download": "Download notes",
        "trash-can": "Delete note"
    }

    def parse_json_notes(self):
        with open("data/notes.json", encoding='utf-8') as notes:
            all_notes = json.load(notes)

        for e in all_notes:
            self.note_list.add_widget(
                TwoLinedItemWithID(text=e["note_title"], secondary_text="Created at: " + e["pub_date"], note=e)
            )

    def load_notes(self, path_to_file="data/notes.json"):
        json_notes = ConnectionController.pull_notes()
        with open(path_to_file, 'w', encoding='utf-8') as file:
            json.dump(json_notes, file, ensure_ascii=False, indent=4)

    def save_input(self):
        if not self.redacted_title.text:
            return

        with open("data/active_note.json", encoding='utf-8') as file:
            note = json.load(file)
            with open("data/notes.json", encoding='utf-8') as notes:
                all_notes = json.load(notes)

            if note in all_notes:
                ConnectionController.patch_note(note["id"], self.redacted_text.text)
                ConnectionController.rename_note(note["id"], self.redacted_title.text)
            else:
                ConnectionController.create_note(self.redacted_title.text, self.redacted_text.text)

            for e in self.note_list.walk():
                self.note_list.remove_widget(e)

    def delete_current(self):
        with open("data/active_note.json", encoding='utf-8') as file:
            note = json.load(file)
            ConnectionController.delete_note(note["id"])

            for e in self.note_list.walk():
                self.note_list.remove_widget(e)
            self.load_notes()
            self.parse_json_notes()

    def button_callback(self, instance):
        if instance.icon == "trash-can":
            self.delete_current()

        if instance.icon == "pencil":
            self.transition = SlideTransition()

            with open("data/active_note.json", encoding='utf-8') as file:
                note = json.load(file)

            self.redacted_text.text = note["note_title"]
            self.redacted_title.text = note["note_text"]
            self.current = "EditScreen"

        if instance.icon == "plus":
            self.transition = SlideTransition()
            self.redacted_text.text = ""
            self.redacted_title.text = ""
            self.current = "EditScreen"
            with open('data/active_note.json', 'w', encoding='utf-8') as file:
                x = json.loads("{}")
                json.dump(x, file, ensure_ascii=False, indent=4)

        if instance.icon == "cloud-download":
            # TODO: исправить костыль
            for e in self.note_list.walk():
                self.note_list.remove_widget(e)

            self.load_notes()
            self.parse_json_notes()


class TwoLinedItemWithID(TwoLineListItem):
    def __init__(self, note=None, **kwargs):
        super().__init__(**kwargs)
        self.note = note
        self.request_new_screen = 0

    def on_click(self):
        with open("data/active_note.json", 'w', encoding='utf-8') as file:
            json.dump(self.note, file, ensure_ascii=False, indent=4)

    def request_screen_change(self):
        self.request_new_screen = 0
