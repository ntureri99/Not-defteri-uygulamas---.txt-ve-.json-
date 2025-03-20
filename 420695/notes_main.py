from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QVBoxLayout, QHBoxLayout, QFormLayout
import json

app = QApplication([])

# Uygulama arayüzü
notes_win = QWidget()
notes_win.setWindowTitle("Akıllı Notlar")
notes_win.resize(900, 600)

# Widgetlar
list_notes = QListWidget()
list_notes_label = QLabel("Notların Listesi")
button_note_create = QPushButton("Not Oluştur")
button_note_del = QPushButton("Notu Sil")
button_note_save = QPushButton("Notu Kaydet")
list_tags = QListWidget()
list_tags_label = QLabel("Etiket Listesi")
button_tag_add = QPushButton("Nota Ekle")
button_tag_del = QPushButton("Nottan Çıkar")
button_tag_search = QPushButton("Notları Etikete Göre Ara")
field_tag = QLineEdit()
field_tag.setPlaceholderText("Etiketi giriniz")
field_text = QTextEdit()

# Düzenler
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)

row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)

col_2.addLayout(row_1)
col_2.addLayout(row_2)
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)

row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layout_notes)

# Fonksiyonlar
def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Not Ekle", "Notun adı: ")
    if ok and note_name:
        notes[note_name] = {"metin": "", "etiketler": []}
        list_notes.addItem(note_name)
        print(notes)

def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["metin"])
    list_tags.clear()
    list_tags.addItems(notes[key].get("etiketler", []))  # Varsayılan olarak boş liste


def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["metin"] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes.keys())
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if tag and tag not in notes[key]["etiketler"]:
            notes[key]["etiketler"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)

def del_tag():
    if list_notes.selectedItems() and list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["etiketler"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["etiketler"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == "Notları Etikete Göre Ara" and tag:
        notes_filtered = {key: value for key, value in notes.items() if tag in value["etiketler"]}
        button_tag_search.setText("Aramayı Sıfırla")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered.keys())
    elif button_tag_search.text() == "Aramayı Sıfırla":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        button_tag_search.setText("Notları Etikete Göre Ara")
        list_notes.addItems(notes.keys())

# Olayları bağlama
button_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

# Uygulamayı başlatma
notes_win.show()
try:
    with open("notes_data.json", "r") as file:
        notes = json.load(file)
    list_notes.addItems(notes.keys())
except FileNotFoundError:
    notes = {}

app.exec_()
