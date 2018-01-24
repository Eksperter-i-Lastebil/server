# -*- coding: utf-8 -*-
"""
Created on Wednesday Jan 24 2018

Module for snapping lat-lng coordinates to roads using Google Maps Roads API
"""

import googlemaps


def snap_to_road(data, interpolate=False):
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
    gmaps = googlemaps.Client(key='AIzaSyD8IMQPEn0qiIw144Sv7hrYDtcGcb7mcvk')
    chunks = []
    for i in range(0, len(data), 100):
        chunks.append(gmaps.snap_to_roads(
            data[i:i + 100], interpolate=interpolate))
    road = []
    for chunk in chunks:
        road += chunk
    return road
