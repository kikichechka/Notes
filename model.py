import xml.etree.ElementTree as ET

class Record:
    def __init__(self, title, description, datetime):
        self.title = title
        self.description = description
        self.datetime = datetime

    def toElementTree(self):
        record = ET.Element("record")
        record_title = ET.Element("title")
        record_description = ET.Element("description")
        record_datetime = ET.Element("datetime")

        record.append(record_title)
        record.append(record_description)
        record.append(record_datetime)

        record_title.text = self.title
        record_description.text = self.description
        record_datetime.text = self.datetime

        return record

    def __str__(self):
        text = f"{self.title} {self.description} {self.datetime}"
        return text

    @classmethod
    def fromElementTree(cls, elem):
        if type(elem) != ET.Element:
            return None
        title = None
        description = None
        datetime = None
        for current in elem:
            if current.tag == "title":
                title = current.text
            elif current.tag == "description":
                description = current.text
            elif current.tag == "datetime":
                datetime = current.text

        return cls(title, description, datetime)


class Notes:
    _instance = None
    _file_name = "text.txt"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.__records = list()
        self.reestablish()

    def reestablish(self):
        self.__records = list()
        try:
            tree = ET.parse(self._file_name)
        except:
            return
        records = tree.findall('record')
        for record in records:
            obj_record = Record.fromElementTree(record)
            self.__records.append(obj_record)


    def __str__(self):
        records = self.get_records()
        text = "|{0:3} | {1:15} | {2:15} | {3:30}|".format("#", "Заголовок", "Описание", "Время")
        count_ = len(text)
        text += "\n{0:30}".format(count_ * "-")
        for index, record in enumerate(records):
            text += "\n|{0:3} | {1:15} | {2:15} | {3:30}|".format(index + 1, record.title, record.description, record.datetime)
        return text

    def __repr__(self):
        return self.__str__()

    def dump(self):
        elem = self.toElementTree()
        tree = ET.ElementTree(elem)
        tree.write(self._file_name, encoding='utf-8')

    def toElementTree(self):
        records = self.__records
        elem_notes = ET.Element("notes")
        for record in records:
            elem_record = record.toElementTree()
            elem_notes.append(elem_record)
        return elem_notes

    def get_records(self):
        return self.__records

    def add_record(self, record):
        self.__records.append(record)

    def validate_index(self, index):
        if type(index) != int:
            raise ValueError("Тип индекса должен быть целым числом")

        if (index > 0) and index > len(self.__records) - 1:
            raise ValueError("Индекс выходит за границы")
        elif index < 0 and abs(index) > len(self.__records):
            raise ValueError("Индекс выходит за границы")

    def __getitem__(self, item):
        self.validate_index(item)
        return self.__records[item]

    def __setitem__(self, key, value):
        if type(value) is not Record:
            raise ValueError("Тип значения должен быть объект класса Record")
        self.validate_index(key)
        self.__records[key] = value

    def __delitem__(self, key):
        self.validate_index(key)
        del self.__records[key]

    def __len__(self):
        return len(self.__records)