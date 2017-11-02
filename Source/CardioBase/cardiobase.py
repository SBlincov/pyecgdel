# -*- coding: utf-8 -*-



from Source.CardioBase.cardiobase_python import CardioBase
from Source.CardioBase.cardiodata import CardioData, CardiobaseError
from _pickle import dumps, loads
import json


#   Класс работы с базой
class Cardiobase():
    _id_columns_hash = 20
    _id_columns_hash_json = 27
    _id_ml_info_hash_json = 29

    #   Конструктор
    def __init__(self):
        self._cardiobase = CardioBase()
        self.leads = ["i", "ii", "iii", "avr", "avl", "avf", "v1", "v2", "v3", "v4", "v5", "v6"]
        self._cardiodata = CardioData()
        self.dict_types = dict()
        self.dict_types["default"] = 276

    #   Подключаемся к базе
    def connect(self, ip="10.0.30.30"):
        self._cardiobase.connect(ip)
        columns = self.get_hash(Cardiobase._id_columns_hash)
        columns_json = self._cardiobase.get_hash(Cardiobase._id_columns_hash_json)
        self._cardiodata.set_dictionary(columns, columns_json)

    #   Отключаемся от базы
    def disconnect(self):
        self._cardiobase.disconnect()

    #   Возвращаем информацию об пациенте по id
    def get_patient(self, id_patient):
        return self._cardiobase.get_patient(id_patient)

    #   Есть ли пациент с таким id?
    def check_patient_exist(self, id_patient):
        return self._cardiobase.check_patient_exist(id_patient)

    #   Возвращаем список пациентов
    def get_patient_list(self):
        return self._cardiobase.get_patient_list()

    #   Создаем файл
    def create_file(self, id_patient, fname, type_id_str="default", user_id=1):
        list_keys = list(self.dict_types.keys())
        if type_id_str in list_keys:
            type_id = self.dict_types[type_id_str]
            return self._cardiobase.create_file(id_patient, fname, type_id, user_id)
        else:
            CardioError = CardiobaseError("Нет типа данных '" + type_id_str + "'. Используйте " + str(list_keys))
            raise CardioError


            #   Закрываем файл

    def close_file(self, file_id):
        return self._cardiobase.close_file(file_id)

    #   Берем массив данных
    def bulk_data_get(self, columns, additionally=""):
        nums = [self._cardiodata.get_index(col) for col in columns]
        data = self._cardiobase.bulk_data_get(nums, additionally)
        for file_id in data['data']:
            for i, info in enumerate(file_id):
                if info is not None:
                    if nums[i] <= 1000:
                        file_id[i] = loads(info.encode('ISO-8859-1'))
                    else:
                        file_id[i] = json.loads(info)
        return data

    #   Устанавливаем массив данных
    def bulk_data_set(self, data):
        data_list = []
        for key, column in data.items():
            for value in column:
                index = self._cardiodata.check_and_get_index(key, value[1])
                if (index <= 1000):
                    data_list.append([value[0], index, dumps(value[1], 2).decode('ISO-8859-1')])
                else:
                    data_list.append([value[0], index, json.dumps(value[1])])
        self._cardiobase.bulk_data_set(data_list)

    #   Удалить все записи по id
    def delete(self, file_id, column=None):
        if column is None:
            self._cardiobase.delete_id(file_id)
        else:
            num = self._cardiodata.get_index(column)
            self._cardiobase.delete_id_num(file_id, num)

    # Возвращаем список файлов с заданным type_id
    def get_files(self, type_id, begin_date="01.01.1000, 00:00:00", end_date="01.01.3000, 00:00:00", user_id=602669172):
        return self._cardiobase.get_files(type_id, begin_date, end_date, user_id)

    #   Возвращает id файла по его имени
    def get_file_id(self, fname, user_id=602669172):
        return self._cardiobase.get_file_id(fname, user_id)

    #   Создаем пациента
    def create_patient(self, fio, birthday, gender):
        return self._cardiobase.create_patient(fio, birthday, gender)

    #   Вернуть информацию о столбцах
    def get_columns(self):
        return self._cardiodata.get_columns()

    #   Зафиксировать изменения в базе
    def commit(self):
        self._cardiobase.commit()

    #   Создать строку хеш-таблицы
    def insert_hash_row(self, id_type_hash, id_, name, data):
        return self._cardiobase.insert_hash_row(id_, id_type_hash, name, dumps(data, 2).decode('ISO-8859-1'))

    #   Удалить строку хеш-таблицы
    def delete_hash_row(self, id_type_hash, id_):
        return self._cardiobase.delete_hash_row(id_, id_type_hash)

    #   Создать хеш-таблицу
    def create_type_hash(self, name):
        return self._cardiobase.create_type_hash(name)

    #   Вернуть все запиcи хеш-таблицы
    def get_hash(self, id_type_hash):
        hash_table = self._cardiobase.get_hash(id_type_hash)
        for i, info in enumerate(hash_table['data']):
            if id_type_hash != self._id_ml_info_hash_json and id_type_hash != self._id_columns_hash_json:
                hash_table['data'][i] = loads(info.encode('ISO-8859-1'))
            else:
                hash_table['data'][i] = json.loads(info)
        return hash_table

    #   Обновить данные в строке хеш-таблицы
    def update_hash_row_data(self, id_type_hash, id_, data):
        return self._cardiobase.update_hash_row(id_, id_type_hash, "", dumps(data, 2).decode('ISO-8859-1'), 0, 1)

    #   Обновить имя строки хеш-таблицы
    def update_hash_row_name(self, id_type_hash, id_, name):
        return self._cardiobase.update_hash_row(id_, id_type_hash, name, dumps("", 2).decode('ISO-8859-1'), 1, 0)

    #   Загрузить edf файла id_file локально по пути fname
    def read_edf(self, id_file):
        return self._cardiobase.read_edf(id_file)

    #   Сгенерировать событие в базе
    def cardio_event(self, object_name, event_name, id_file):
        self._cardiobase.cardio_event(object_name, event_name, id_file, "diagnostics")

    #   Получить диагноз по файлу
    def get_diagnosis(self, id_file):
        return self._cardiobase.get_diagnosis(id_file)

    #   Записать диагноз по файлу
    def set_diagnosis(self, id_file, diagnosis):
        self._cardiobase.set_diagnosis(id_file, diagnosis)


