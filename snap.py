# -*- coding: utf-8 -*-
"""
Created on Wednesday Jan 24 2018

Module for snapping lat-lng coordinates to roads using Google Maps Roads API
"""

import numpy as np
import googlemaps


def snap_to_road(data, interpolate=False, chunk_size=100):
    """Snaps lat-lng coordinates to roads using Google Maps Roads API.

    Parameters:
        data        : 2D list, each row in the matrix is a list of length 2,
                      containing latitude and longitude
        interpolate : bool, optional, whether to interpolate a path to include
                      all points forming the full road-geometry. When true,
                      additional interpolated points will also be returned,
                      resulting in a path that smoothly follows the geometry
                      of the road, even around corners and through tunnels.
                      Interpolated paths may contain more points than the
                      original path.

    Returns:
        A list containing information on the snapped points.
    """
    coords = data[:, 1:3]
    gmaps = googlemaps.Client(key='AIzaSyD8IMQPEn0qiIw144Sv7hrYDtcGcb7mcvk')
    chunks = []
    for i in range(0, len(coords), chunk_size):
        chunks.append(gmaps.snap_to_roads(
            coords[i:i + chunk_size], interpolate=interpolate))

    road = []
    j = 0
    for i in range(0, len(coords), chunk_size):
        road.append(reformat_data(data[i:i + chunk_size], chunks[j]))
        j += 1
    road = np.concatenate(road)
    return road

def reformat_data(data, road):
    new_data = data[:1, :]
    prev_original = 0
    for i in range(1, len(road)):
        if 'originalIndex' in road[i].keys():
            id_ = road[i]['originalIndex']
            if i > prev_original + 1:
                new_coords = np.concatenate([data[id_:id_ + 1, :] for _ in range(i - prev_original - 1)])
                for j, row in enumerate(new_coords):
                    row[1] = road[id_ + j]['location']['latitude']
                    row[2] = road[id_ + j]['location']['longitude']
                new_data = np.concatenate((new_data, new_coords))
            new_data = np.concatenate((new_data, data[id_:id_ + 1, :]))
            prev_original = i
    return new_data


#
# import time
# import datetime
# import numpy as np
# data = np.loadtxt('test-data.txt', delimiter=' , ')
#
# id_ = np.arange(data.shape[0], dtype=np.int32)
# id_ = np.reshape(id_, (id_.shape[0], 1))
# id_[:20] = 0
# id_[20:] = 1
#
# timestamps = [datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') for _ in range(data.shape[0])]
# timestamps = np.reshape(np.array(timestamps), (data.shape[0], 1))
# timestamps.shape
#
# datatypes = ['brøyte', 'skrape', 'strø', 'salt']
# types = [datatypes[np.random.randint(0, len(datatypes))] for _ in range(data.shape[0])]
# types = np.reshape(np.array(types), (data.shape[0], 1))
#
# data = np.concatenate((id_, data, timestamps, types), axis=1)
# data.shape
#
# new_data = snap_to_road(data, interpolate=True, chunk_size=10)
# print(data.shape)
# print(new_data.shape)
# print(new_data)
#
# with open('test1.txt', mode='w') as f:
#     for row in new_data:
#         f.write(str(row)[1:-1].replace('\'', '').replace(' ', ',') + '\n')
