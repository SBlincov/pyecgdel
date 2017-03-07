# -*- coding: utf-8 -*-



import numpy as np



class CardiobaseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)



class CardioData: 

    
    #   Конструктор
    def __init__(self):
        self._dictionary = {}

        
    #   Загружаем словарь
    def set_dictionary(self, columns):
        self._dictionary = {}
        for i, name in enumerate(columns['name']):
            self._dictionary[name] = (columns['id'][i], columns['data'][i])          
    

    #   Возвращает индекс в базе по названию признака
    #   и проверяет data на соответствие типа  
    def check_and_get_index(self, column, data):
        try:
            index = self._dictionary[column][0]
        except KeyError:
            raise CardiobaseError("Нет столбца с именем '" + column + "'")
        self._checkType(column, data, self._dictionary[column][1])
        return index
        
        
    #   Возвращает индекс в базе по названию признака
    def get_index(self, column):
        try:
            index = self._dictionary[column][0]
        except KeyError:
            raise CardiobaseError("Нет столбца с именем '" + column + "'")
        return index


    #   Проверяет соответствие данных типу data_type
    def _checkType(self, column, data, data_type):
        
        _type = data_type[0]
        if not isinstance(data, _type):
                raise CardiobaseError("Ошибка типа данных (столбец '" + column +
                "'), ожидался " + str(_type) + ', получен ' + str(type(data)))
        
        if _type == np.ndarray:
            ndarray_type = data_type[1]
            if not issubclass(data.dtype.type, ndarray_type):
                raise CardiobaseError("Ошибка типа элементов (столбец '" + column +
                "'), ожидался " + str(ndarray_type) + ', получен ' + str(data.dtype.type))
            dim = len(data_type[2])
            if dim != data.ndim:
                raise CardiobaseError("Ошибка размерности массива (столбец '" + column +
                "'), ожидалась размерность " + str(dim) + ", получена размерность " + str(data.ndim))
            if dim == 1:
                size = data_type[2][0]
                if size != None and size != len(data):
                    raise CardiobaseError("Ошибка длины вектора (столбец '" + column +
                    "'), ожидалась " + str(size) + ", получена " + str(len(data)))
            if dim == 2:
                rows = data_type[2][0]
                cols = data_type[2][1]
                if rows != None and rows != data.shape[0]:
                    raise CardiobaseError("Ошибка размера матрицы (столбец '" + column +
                    "'), ожидалось " + str(rows) + " строк, получено " + str(data.shape[0]))
                if cols != None and cols != data.shape[1]:
                    raise CardiobaseError("Ошибка размера матрицы (столбец '" + column +
                    "'), ожидалось " + str(cols) + " столбцов, получено " + str(data.shape[1]))
        
        if _type == list:
            list_type = data_type[1]
            if list_type == "characteristics":
                if len(data) != 2:
                    raise CardiobaseError("Ошибка размера списка (столбец '" + column +
                    "'), ожидалось 2, получено " + str(len(data)))
                if not isinstance(data[0], list) or not isinstance(data[1], list):
                    raise CardiobaseError("Ошибка содержания списка (столбец '" + column +
                    "'), ожидались 2 списка")
                if len(data[0]) != len(data[1]):
                    raise CardiobaseError("Размеры списков должны совпадать")
                if not all(isinstance(x, str) for x in data[0]):
                    raise CardiobaseError("Ошибка содержания первого списка (столбец '" + column +
                    "'), ожидались str")
                if not all(isinstance(x, float) or x==None for x in data[1]):
                    raise CardiobaseError("Ошибка содержания второго списка (столбец '" + column +
                    "'), ожидались float")

    
    #   Извлекаем информацию о столбцах базы
    def get_columns(self):
        result = {}
        for key, value in self._dictionary.items():
            result[key] = value[1]
        return result


