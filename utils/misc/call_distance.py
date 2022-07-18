import math
from math import cos, sin
from data.locatiions import Job

R = 6378.1


def calc_distance(lat1, long1, lat2, long2):
    lat1 = math.radians(lat1)
    long1 = math.radians(long1)

    lat2 = math.radians(lat2)
    long2 = math.radians(long2)
    # haversine formula
    dlon = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # Radius of earth in kilometers is 6371
    dictance = c * R

    return dictance


def choose_shortest(latitude: float, longitude: float):
    distances = list()
    for job_name, location_job in Job:
        distances.append((job_name,
                          calc_distance(latitude, longitude,
                                        location_job["lat"], location_job["long"])
                          ))
    return distances
