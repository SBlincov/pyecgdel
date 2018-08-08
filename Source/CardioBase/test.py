# -*- coding: utf-8 -*-


from cardiobase import Cardiobase


cb = Cardiobase()

#Подключаемся к базе
cb.connect()

#Получаем информацию о пациенте с id=1
patient_info = cb.get_patient(1)

#Есть ли пациент с id=10?
is_exist = cb.check_patient_exist(10)

#Получаем список id всех пациентов
patients = cb.get_patient_list()

#Получаем список всех возможных столбцов измерения
columns = cb.get_columns()

#Получаем характеристики отведения v1 и диагноз по всех измерениям,
#где есть хотя бы один из запрашиваемых столбцов 
data = cb.bulk_data_get(["diagnosis"], "cardio_file.id < 2000")

#Отключаемся от базы
cb.disconnect()

print("Тест пройден!")


