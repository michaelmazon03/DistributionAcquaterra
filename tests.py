#file test.py
from distribution_acquaterra import sort_coordinates
from distribution_acquaterra import pixels_inundated
import numpy as np
import pytest
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


def test_sorting_lat_is_correct():
    long=[250., 300., 280.]
    lat=[30., -30.5, 20.5]
    sort_coordinates(long1,lat1)


    
    assert [long, lat]==[[300., 280., 250.],[-30.5., 20.5, 30.]]
    assert [long, lat]!=[[250., 300., 280.],[30., -30.5, 20.5]]

def test_sorting_long_is_correct():
    long=[250., 300., 280.]
    lat=[30., 30., 30.]
    sort_coordinates(long,lat)

    assert [long1, lat1]==[[250., 280., 300.],[30.., 30., 30.]]
    assert [long1, lat1]!=[[250., 300., 280.],[30., -30.5, 20.5]]

def test_sorting_latitudes_already_sorted():
    initial_lat=[10., 20., 30.]
    initial_long=[10.,10.,10.]
    lat_var=initial_lat
    long_var=initial_long
    sort_coordinates(long_var,lat_var)
    
    assert [long_var, lat_var]==[initial_long, initial_lat]

def test_sorting_longitudes_already_sorted():
    initial_lat=[10.,10.,10.]
    initial_long=[100.,200.,300.]
    
    lat_var=initial_lat
    long_var=initial_long
    sort_coordinates(long_var,lat_var)

    assert [long_var, lat_var]==[initial_long, initial_lat]
    
def test_determination_pixels_inundated_is_correct():
    
    
    

