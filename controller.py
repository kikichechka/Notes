import model as m

nt = m.Notes()
# 1. Вывод списка заметок
def show_notes():
    records = nt.get_records()
    nt.dump()
    return records

# 2. Добавление заметки
def input_note(title, description, datetime):
    record = m.Record(title, description, datetime)
    nt.add_record(record)
    nt.dump()

#3. Удаление записи
def delеtе_note(index):
    nt.__delitem__(index)
    nt.dump()

#4. Поиск по индексу
def search_note_by_id(index):
    return show_notes()[index]
    
# 6. Поиск посимвольно
def search_note(string):
    records = nt.get_records()
    result = list()
    for index, record in enumerate(records):
        title = record.title
        description = record.description
        if string.lower() in title.lower() or string in description.lower():
            result.append(record)
    return result

#7. Редактирование
def change_note(index, title, description, datetime):
    # datetime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    record_new = m.Record(title, description, datetime)
    nt[index] = record_new
    nt.dump()
