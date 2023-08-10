import json
from datetime import datetime


class Note:
    def __init__(self, title, body):
        self.id = None
        self.title = title
        self.body = body
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return f'[{self.id}] {self.title} ({self.timestamp})\n{self.body}'


class NotesApp:
    def __init__(self):
        self.notes = []
        self.load_notes()

    def load_notes(self):
        try:
            with open('notes.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                for note_data in data:
                    note = Note(note_data['title'], note_data['body'])
                    note.id = note_data['id']
                    note.timestamp = note_data['timestamp']
                    self.notes.append(note)
        except FileNotFoundError:
            pass

    def save_notes(self):
        data = []
        for note in self.notes:
            data.append({
                'id': note.id,
                'title': note.title,
                'body': note.body,
                'timestamp': note.timestamp
            })
        with open('notes.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def add_note(self, title, body):
        note = Note(title, body)
        if not self.notes:
            note.id = 1
        else:
            note.id = max([note.id for note in self.notes]) + 1
        self.notes.append(note)
        self.save_notes()
        print(f'Заметка {note.id} добавлена.')

    def view_notes(self):
        if not self.notes:
            print('Заметки не найдены.')
            return
        for note in self.notes:
            print(note)
            print()

    def view_note(self, id):
        for note in self.notes:
            if note.id == id:
                print(note)
                return
        print(f'Заметка {id} не найдена.')

    def view_note_for_data(self, timestamp):
        search_date = datetime.strptime(timestamp, '%Y-%m-%d').date()
        matching_notes = []

        for note in self.notes:
            note_date = datetime.strptime(note.timestamp, '%Y-%m-%d %H:%M:%S').date()
            if note_date == search_date:
                matching_notes.append(note)

        if matching_notes:
            for note in matching_notes:
                print(note)
        else:
            print(f'Заметки для {timestamp} не найдены.')

    def edit_note(self, id, title=None, body=None):
        for note in self.notes:
            if note.id == id:
                if title is not None:
                    note.title = title
                if body is not None:
                    note.body = body
                note.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_notes()
                print(f'Заметка {id} изменена.')
                return
        print(f'Заметка {id} не найдена.')

    def delete_note(self, id):
        for i, note in enumerate(self.notes):
            if note.id == id:
                del self.notes[i]
                self.save_notes()
                print(f'Заметка {id} удалена.')
                return
        print(f'Заметка {id} не найдена.')


def display_menu():
    print('1. Показать все заметки')
    print('2. Добавить заметку')
    print('3. Редактировать заметку')
    print('4. Удалить заметку')
    print('5. Вывести одну заметку')
    print('6. Поиск заметки по дате')
    print('7. Выход')
    print()


while True:
    display_menu()
    app = NotesApp()
    choice = input('Введите номер команды: ')
    if choice == '1':
        app.view_notes()
    elif choice == '2':
        title = input('Введите заголовок: ')
        body = input('Введите тело заметки: ')
        app.add_note(title, body)
    elif choice == '3':
        id = int(input('Введите id: '))
        title = input('Введите новый заголовок (или оставте пустым, чтобы сохранился прежний): ')
        body = input('Введите тело заметки (или оставте пустым, чтобы сохранилось прежним): ')
        app.edit_note(id, title or None, body or None)
    elif choice == '4':
        id = int(input('Введите id: '))
        app.delete_note(id)
    elif choice == '5':
        id = int(input('Введите id: '))
        app.view_note(id)
    elif choice == '6':
        timestamp = str(input('Введите дату заметки(yyyy-mm-dd): '))
        app.view_note_for_data(timestamp)
    elif choice == '7':
        break
