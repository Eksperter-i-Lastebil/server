# -*- coding: utf-8 -*-
"""
Created on Wednesday Jan 24 2018

Module for snapping lat-lng coordinates to roads using Google Maps Roads API
"""

import googlemaps


def snap_to_road(data, interpolate=False):
    gmaps = googlemaps.Client(key='AIzaSyD8IMQPEn0qiIw144Sv7hrYDtcGcb7mcvk')
    chunks = []
    for i in range(0, len(data), 100):
        chunks.append(gmaps.snap_to_roads(
            data[i:i + 100], interpolate=interpolate))
    road = []
    for chunk in chunks:
        road += chunk
    return road
