# -*- coding: utf-8 -*-
"""
Created on Wednesday Jan 31 2018

Utility functions
"""

import time
import datetime
import numpy as np

def gen_test_data_from_coords(filename):
    data = np.loadtxt(filename, delimiter=' , ')

    id_ = np.arange(data.shape[0], dtype=np.int32)
    id_ = np.reshape(id_, (id_.shape[0], 1))
    # id_[:20] = 0
    # id_[20:] = 1

    timestamps = [datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S') for _ in range(data.shape[0])]
    timestamps = np.reshape(np.array(timestamps), (data.shape[0], 1))
    timestamps.shape

    datatypes = ['brøyte', 'skrape', 'strø', 'salt']
    types = [datatypes[np.random.randint(0, len(datatypes))] for _ in range(data.shape[0])]
    types = np.reshape(np.array(types), (data.shape[0], 1))

    data = np.concatenate((id_, data, timestamps, types), axis=1)
    return data

def save_data(filename, data):
    with open(filename, mode='w') as f:
        for row in data:
            f.write(str(row)[1:-1].replace('\'', '').replace('\n', '').replace(' ', ',') + '\n')

def load_data(filename, delimiter=','):
    return np.loadtxt(filename, delimiter=delimiter, dtype=np.str)

test_data = gen_test_data_from_coords('test-data.txt')
save_data('test-data-1.txt', test_data)

from snap import *
new_data = snap_to_road(test_data, interpolate=True, chunk_size=100)
save_data('road-data-1.txt', new_data)

a = load_data('road-data-1.txt', delimiter=',')
