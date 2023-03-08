import datetime
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget, IconLeftWidget
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.toolbar import MDBottomAppBar
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.config import Config
import controller
from kivy.core.window import Window
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Window.size = (400, 620)

class Tab(MDFloatLayout, MDTabsBase):
    pass

class ShowAllNotes(MDBoxLayout):
    list_notes: ObjectProperty()
    text_field: ObjectProperty()
    button_magnify: ObjectProperty()

class ShowNote(MDBoxLayout):
    title: ObjectProperty()
    description: ObjectProperty()
    datetime: ObjectProperty()

class ChangeNote(BoxLayout):
    title: StringProperty()
    description: StringProperty()
    datetime: StringProperty()

class Topappbar(MDBottomAppBar):
    action_button: ObjectProperty()

class Container(MDBoxLayout):
    action_button = ObjectProperty()
    contain = ObjectProperty()
    app_bar = ObjectProperty()
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.draw_coontain()

    def show_alert_dialog_delete_note(self, instance):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Удалить заметку?",
                buttons=[
                    MDFlatButton(
                        text="НЕТ",
                        theme_text_color="Custom",
                        on_release= self.dialog_close,
                    ),
                    MDFlatButton(
                        text="ДА",
                        theme_text_color="Custom",
                        on_release= lambda x: self.delete_note(instance),
                    ),
                ],
            )
        self.dialog.open()
        
    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)
    
    def delete_note(self, instance):
        self.dialog_close()
        controller.delеtе_note(int(instance.id))
        self.draw_coontain()

    def search_item_by_index(self, index):
        note = controller.search_note_by_id(index)
        return note

    index_note = 0
    def change_main_icon_action_button(self, instance):
        self.index_note = int(instance.id)
        self.action_button.icon = "pencil"
        self.change_widget(self.index_note)
        self.action_button.left_action_items= [["arrow-left", lambda x: self.draw_coontain()]]
    
    def change_icon_action_button(self):
        if self.action_button.icon == "pencil":
            self.action_button.icon = "check"
            self.change_widget(self.index_note)
        elif self.action_button.icon == "check":
            if self.change_note != None and self.change_note.title.text != "" and self.change_note.description.text != "":
                self.save_change_note()
                self.draw_coontain()
                self.action_button.icon = "plus"
            elif self.new_note != None:
                self.save_new_note()
                self.draw_coontain()
                self.action_button.icon = "plus"
        elif self.action_button.icon == "plus":
            self.change_widget(self.index_note)
            self.action_button.left_action_items= [["arrow-left", lambda x: self.draw_coontain()]]
            self.action_button.icon = "check"
            

    change_note = None
    new_note = None
    def change_widget(self, index):
        if self.action_button.icon == "pencil":
            item_note = self.search_item_by_index(index)
            self.contain.clear_widgets()
            show_note = ShowNote(orientation= 'vertical')
            show_note.title.text = item_note.title
            show_note.description.text += item_note.description
            show_note.datetime.text += item_note.datetime
            self.contain.add_widget(show_note)
        elif self.action_button.icon == "check":
            item_note = self.search_item_by_index(index)
            self.contain.clear_widgets()
            self.change_note = ChangeNote(orientation= 'vertical')
            self.change_note.title.text += item_note.title
            self.change_note.description.text += item_note.description
            self.change_note.datetime.text += f"\n{item_note.datetime}"
            self.contain.add_widget(self.change_note)
        elif self.action_button.icon == "plus":
            self.contain.clear_widgets()
            time = datetime.datetime.now()
            self.new_note = ChangeNote(orientation= 'vertical')
            self.new_note.title.text += ""
            self.new_note.description.text += "" 
            self.new_note.datetime.text += time.strftime("%d-%m-%Y %H:%M")
            self.contain.add_widget(self.new_note)
    
    def save_change_note(self):
        title = self.change_note.title.text
        description = self.change_note.description.text
        datetime = self.change_note.datetime.text
        controller.change_note(self.index_note, title, description, datetime)
        self.change_note = None
    
    def save_new_note(self):
        title = self.new_note.title.text
        description = self.new_note.description.text
        datetime = self.new_note.datetime.text
        controller.input_note(title, description, datetime)
        self.new_note = None

    all_notes = None
    def draw_coontain(self): 
        self.contain.clear_widgets()
        self.action_button.left_action_items= [["", lambda x: x]]
        self.action_button.icon = "plus"
        self.all_notes = ShowAllNotes(orientation= 'vertical')
        self.all_notes.button_magnify.on_release = self.draw_item_note
        self.contain.add_widget(self.all_notes)
        self.draw_item_note()
    
    def draw_item_note(self):
        self.all_notes.list_notes.clear_widgets()
        lst = self.search_note()
        for index, note in enumerate(lst):
            self.all_notes.list_notes.add_widget(
                TwoLineAvatarIconListItem(
                    IconRightWidget(
                        id= str(index),
                        icon="delete",
                        icon_size= "15sp",
                        on_press= self.show_alert_dialog_delete_note
                    ),
                    text= note.title,
                    secondary_text= note.description,
                    id= str(index),
                    on_release= self.change_main_icon_action_button
                )
            )
        
    def search_note(self):
        lst = list()
        if self.all_notes.text_field.text == "":
            lst = controller.show_notes()
        else:
            string = self.all_notes.text_field.text
            lst = controller.search_note(string)
        return lst  
            