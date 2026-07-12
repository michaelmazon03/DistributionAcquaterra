#file test.py
from distribution_acquaterra import sort_coordinates

def generate_coord():
    long=150.
    lat=45.
    return [long,lat]


###########################################


def test_longitude_is_valid():
    coord=generate_coord()
    assert coord[0]>0. and coord[1]<360.

def test_latitude_is_valid():
    coord=generate_coord()
    assert coord[1]>-90. and coord[1]<90.

def test_coord_type():
    coord=generate_coord()
    assert type(coord[0])==<class 'float'> and type(coord[1]) == <class 'float'>

