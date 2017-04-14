"""
Вспомогательные функции, связывающие пересечения нуля и экстремумы детализирующих вейвлет-коэффииентов.

Входные параметры:
    wdc - детализирующие вейвлет-коэффициенты.
    begin_index - индекс начала поиска.
    end_index - индекс конца поиска.
    window - окно поиска.
    zcs - список пересечений нуля.
"""

from Source.Model.main.zero_crossings.zero_crossing import *
from ..params.common import *


def get_zcs_with_global_mms(wdc, begin_index, end_index):

    zcs = get_zcs_only_indexes(wdc, begin_index, end_index)
    init_zcs_with_global_mms(wdc, zcs, begin_index, end_index)

    return zcs


def get_zcs_with_local_mms(wdc, begin_index, end_index):

    zcs = get_zcs_only_indexes(wdc, begin_index, end_index)
    init_zcs_with_local_mms(wdc, zcs, begin_index, end_index)

    return zcs


def get_zcs_with_special_mms(wdc, begin_index, end_index, window):

    zcs = get_zcs_only_indexes(wdc, begin_index, end_index)
    init_zcs_with_special_mms(wdc, zcs, begin_index, end_index, window)

    return zcs


def get_zcs_only_indexes(wdc, begin_index, end_index):

    zcs = []

    signal_index = begin_index

    while signal_index < end_index - 2:

        current_wdc = wdc[signal_index]
        next_wdc = wdc[signal_index + 1]

        if current_wdc * next_wdc < 0:
            zc = ZeroCrossing(signal_index, wdc)
            zcs.append(zc)
            signal_index += 1

        elif abs(next_wdc) < EPSILON:
            zero_period_size = 0

            while abs(next_wdc) < EPSILON and signal_index + 1 + zero_period_size < end_index - 2:
                zero_period_size += 1
                next_wdc = wdc[signal_index + 1 + zero_period_size]

            if current_wdc * next_wdc < 0:
                zc = ZeroCrossing(signal_index + 1 + int((zero_period_size - 1) / 2), wdc)
                zcs.append(zc)

            signal_index = signal_index + 1 + zero_period_size
        else:

            signal_index += 1

    return zcs


def init_zcs_with_global_mms(wdc, zcs, begin_index, end_index):

    if zcs:

        if len(zcs) == 1:
            if zcs[0].index is not begin_index:
                zcs[0].init_global_mm_left(begin_index, wdc)

            if zcs[0].index is not end_index:
                zcs[0].init_global_mm_right(end_index, wdc)

        elif len(zcs) == 2:
            if zcs[0].index is not begin_index:
                zcs[0].init_global_mm_left(begin_index, wdc)
            zcs[0].init_global_mm_right(zcs[1].index, wdc)

            if zcs[-1].index is not end_index:
                zcs[-1].init_global_mm_right(end_index, wdc)
            zcs[-1].init_global_mm_left(zcs[-2].index, wdc)

        else:
            if zcs[0].index is not begin_index:
                zcs[0].init_global_mm_left(begin_index, wdc)
            zcs[0].init_global_mm_right(zcs[1].index, wdc)

            for zc_id in range(1, len(zcs) - 1):
                zcs[zc_id].init_global_mm_left(zcs[zc_id - 1].index, wdc)
                zcs[zc_id].init_global_mm_right(zcs[zc_id + 1].index, wdc)

            if zcs[-1].index is not end_index:
                zcs[-1].init_global_mm_right(end_index, wdc)

            zcs[-1].init_global_mm_left(zcs[-2].index, wdc)

        for zc_id in range(0, len(zcs)):
            zcs[zc_id].init_extremum_sign()


def init_zcs_with_local_mms(wdc, zcs, begin_index, end_index):

    if zcs:
        if len(zcs) == 1:

            if zcs[0].index is not begin_index:
                zcs[0].init_local_mm_left(begin_index, wdc)

            if zcs[0].index is not end_index:
                zcs[0].init_local_mm_right(end_index, wdc)
        elif len(zcs) == 2:

            if zcs[0].index is not begin_index:
                zcs[0].init_local_mm_left(begin_index, wdc)
            zcs[0].init_local_mm_right(zcs[1].index, wdc)

            if zcs[-1].index is not end_index:
                zcs[-1].init_local_mm_right(end_index, wdc)
            zcs[-1].init_local_mm_left(zcs[-2].index, wdc)
        else:

            if zcs[0].index is not begin_index:
                zcs[0].init_local_mm_left(begin_index, wdc)
            zcs[0].init_local_mm_right(zcs[1].index, wdc)

            for zc_id in range(1, len(zcs) - 1):
                zcs[zc_id].init_local_mm_left(zcs[zc_id - 1].index, wdc)
                zcs[zc_id].init_local_mm_right(zcs[zc_id + 1].index, wdc)

            if zcs[-1].index is not end_index:
                zcs[-1].init_local_mm_right(end_index, wdc)

            zcs[-1].init_local_mm_left(zcs[-2].index, wdc)

        for zc_id in range(0, len(zcs)):
            zcs[zc_id].init_extremum_sign()


def init_zcs_with_special_mms(wdc, zcs, begin_index, end_index, window):

    if zcs:
        if len(zcs) == 1:

            if zcs[0].index is not begin_index:
                zcs[0].init_special_mm_left(max(begin_index, zcs[0].index - window), wdc)

            if zcs[0].index is not end_index:
                zcs[0].init_special_mm_right(min(end_index, zcs[0].index + window), wdc)
        elif len(zcs) == 2:

            if zcs[0].index is not begin_index:
                zcs[0].init_special_mm_left(max(begin_index, zcs[0].index - window), wdc)
            zcs[0].init_special_mm_right(min(zcs[1].index, zcs[0].index + window), wdc)

            if zcs[-1].index is not end_index:
                zcs[-1].init_special_mm_right(min(end_index, zcs[-1].index + window), wdc)
            zcs[-1].init_special_mm_left(max(zcs[-2].index, zcs[-1].index - window), wdc)
        else:

            if zcs[0].index is not begin_index:
                zcs[0].init_special_mm_left(max(begin_index, zcs[0].index - window), wdc)
            zcs[0].init_special_mm_right(min(zcs[1].index, zcs[0].index + window), wdc)

            for zc_id in range(1, len(zcs) - 1):
                zcs[zc_id].init_special_mm_left(max(zcs[zc_id - 1].index, zcs[zc_id].index - window), wdc)
                zcs[zc_id].init_special_mm_right(min(zcs[zc_id + 1].index, zcs[zc_id].index + window), wdc)

            if zcs[-1].index is not end_index:
                zcs[-1].init_special_mm_right(min(end_index, zcs[-1].index + window), wdc)
            zcs[-1].init_special_mm_left(max(zcs[-2].index, zcs[-1].index - window), wdc)

        for zc_id in range(0, len(zcs)):
            zcs[zc_id].init_extremum_sign()


