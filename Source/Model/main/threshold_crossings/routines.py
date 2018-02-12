"""
Функции, осуществляющие поиск индексов пересечений детализирующими вейвлет-коэффициентами
некоторого порогового значения.

Входные параметры:
    wdc - детализирующие вейвлет-коэффициенты.
    begin_searching_index - индекс начала поиска.
    end_searching_index - индекс конца поиска.
    threshold - пороговое значение.
"""

from Source.Model.main.params.common import *


def find_left_thc_index(wdc, begin_searching_index, end_searching_index, threshold):

    if begin_searching_index == 0:
        return begin_searching_index

    current_index = begin_searching_index
    prev_index = begin_searching_index - 1

    left_border = max(0, end_searching_index)

    while prev_index > left_border:

        criterion = (wdc[current_index] - threshold) * (wdc[prev_index] - threshold)

        if criterion < 0:
            break
        elif abs(wdc[prev_index] - threshold) < EPSILON:
            threshold_period = 0
            while prev_index >= left_border and abs(wdc[prev_index] - threshold) < EPSILON:
                threshold_period += 1
                prev_index -= 1
        else:
            current_index -= 1
            prev_index -= 1

    return prev_index


def find_right_thc_index(wdc, begin_searching_index, end_searching_index, threshold):

    if begin_searching_index == len(wdc) - 1:
        return begin_searching_index

    current_index = begin_searching_index
    next_index = begin_searching_index + 1

    right_border = min(len(wdc) - 1, end_searching_index)

    while next_index < right_border:

        criterion = (wdc[current_index] - threshold) * (wdc[next_index] - threshold)

        if criterion < 0:
            break
        elif abs(wdc[next_index] - threshold) < EPSILON:
            threshold_period = 0
            while next_index <= right_border and abs(wdc[next_index] - threshold) < EPSILON:
                threshold_period += 1
                next_index += 1
        else:
            current_index += 1
            next_index += 1

    return next_index

