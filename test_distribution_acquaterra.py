#file test.py
from distribution_acquaterra import sort_coordinates
from distribution_acquaterra import pixels_inundated
from distribution_acquaterra import (regional_acquaterra,
                                     mask_pixels_acquaterra,
                                     zonal_acquaterra,
                                     percentage_zonal_distrib_AT)
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
    sort_coordinates(long,lat)


    
    assert [long, lat]==[[300., 280., 250.],[-30.5, 20.5, 30.]]
    assert [long, lat]!=[[250., 300., 280.],[30., -30.5, 20.5]]

def test_sorting_long_is_correct():
    long=[250., 300., 280.]
    lat=[30., 30., 30.]
    sort_coordinates(long,lat)

    assert [long, lat]==[[250., 280., 300.],[30., 30., 30.]]
    assert [long, lat]!=[[250., 300., 280.],[30., -30.5, 20.5]]

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
    common_long=100.
    common_lat=10.
    initial_long=np.array([common_long, 150.])
    initial_lat=np.array([common_lat, 10.])
    end_long=np.array([common_long])
    end_lat=np.array([common_lat])
    long_inundated, lat_inundated=pixels_inundated(initial_long, initial_lat,
                                                  end_long, end_lat)
    assert len(long_inundated)==1
    assert long_inundated[0]==150. and lat_inundated[0]==10.



def test_all_pixels_have_been_inundated():
    initial_lat=np.array([-20.,-10.,10.,20.])
    initial_long=np.array([0.,0.,0.,0.,])
    end_lat=np.array([10.])
    end_long=np.array([10.])
    long_inundated, lat_inundated=pixels_inundated(initial_long, initial_lat,
                                                  end_long, end_lat)

    assert len(long_inundated)==4

def test_no_pixels_have_been_inundated():
    common_lat=[-20.,-10.,10.,20.]
    common_long=[0.,0.,0.,0.,]
    initial_lat=np.array(common_lat)
    initial_long=np.array(common_long)
    end_lat=np.array(common_lat)
    end_long=np.array(common_long)
    long_inundated, lat_inundated=pixels_inundated(initial_long, initial_lat,
                                                  end_long, end_lat)

    assert len(long_inundated)==0

def test_regional_acquaterra_works():
    lat_AT=np.array([10.,50.])
    long_AT=np.array([20.,20.])
    lat_min_reg=5.
    lat_max_reg=15.
    long_min_reg=15.
    long_max_reg=25.

    long_regional, lat_regional=regional_acquaterra(long_min_reg, long_max_reg,
                                                    lat_min_reg, lat_max_reg,
                                                    long_AT, lat_AT)

    assert len(lat_regional)==1 and len(long_regional)==1.
    assert lat_regional[0]==10. and long_regional==20.

def test_longitude_on_regional_AT():

    lat_AT=np.array([10.,50.])
    long_AT=np.array([1.,20.])
    lat_min_reg=5.
    lat_max_reg=15.
    long_min_reg=355.
    long_max_reg=5.

    long_regional, lat_regional=regional_acquaterra(long_min_reg, long_max_reg,
                                                    lat_min_reg, lat_max_reg,
                                                    long_AT, lat_AT)

    assert len(lat_regional)==1 and len(long_regional)==1.
    assert lat_regional[0]==10. and long_regional==1.
    
def test_longitude_smaller_than_360_on_region():

    lat_AT=np.array([10.,50.])
    long_AT=np.array([-1.,20.])
    lat_min_reg=5.
    lat_max_reg=15.
    long_min_reg=355.
    long_max_reg=5.

    long_regional, lat_regional=regional_acquaterra(long_min_reg, long_max_reg,
                                                    lat_min_reg, lat_max_reg,
                                                    long_AT, lat_AT)

    assert len(lat_regional)==1 and len(long_regional)==1.
    assert lat_regional[0]==10. and long_regional==-1.

def test_mask_acquaterra_works():
    global_lat=np.array([-60.,-30.,0.,30.,60.])
    global_long=np.array([100.,50.,100.,50.,100.,])
    lat_AT=np.zeros(2)
    long_AT=np.zeros(2)
    lat_AT[0]=global_lat[1]
    long_AT[0]=global_long[1]
    lat_AT[1]=global_lat[3]
    long_AT[1]=global_long[3]

    mask_AT=mask_pixels_acquaterra(long_AT, lat_AT, global_long, global_lat)
    assert len(mask_AT)==5
    assert mask_AT[1] and mask_AT[3]
    assert mask_AT.count(True)==2

def test_zonal_AT_works():
    lat_AT=np.array([-85., -60., -20., 0., 15., 30., 50., 80.])
    long_AT=np.array([10.,10.,10.,10.,10.,10.,10.,10.])
    lat_min=-20.
    lat_max=40.
    long_reg, lat_reg=zonal_acquaterra(lat_min, lat_max, long_AT, lat_AT)
    assert len(long_reg)==3
    assert long_reg[0]==10. and lat_reg[0]==0.
    assert long_reg[1]==10. and lat_reg[1]==15.
    assert long_reg[2]==10. and lat_reg[2]==30.

def test_no_AT_pixels_in_zonal_region():
    lat_AT=np.array([-85., -60., -20., 0., 15., 30., 50., 80.])
    long_AT=np.array([10.,10.,10.,10.,10.,10.,10.,10.])
    lat_min=-10.
    lat_max=-5.
    long_reg, lat_reg=zonal_acquaterra(lat_min, lat_max, long_AT, lat_AT)
    assert len(long_reg)==0


def test_all_AT_pixels_are_in_the_zonal_reg():
    lat_AT=np.array([ -60., -20., 0., 15., 30., 50.])
    long_AT=np.array([10.,10.,10.,10.,10.,10.])
    lat_min=-65.
    lat_max=60.
    long_reg, lat_reg=zonal_acquaterra(lat_min, lat_max, long_AT, lat_AT)
    assert len(long_reg)==6
    assert long_reg.all()==long_AT.all() and lat_reg.all()==lat_AT.all()


def test_percentage_zonal_distrib_AT_works():
    lat_AT=np.array([-85., -60., -20., 0., 15.,16., 30., 50.,55., 80.])
    long_AT=np.array([10.,10.,10.,10.,10.,10.,10.,10.,10.,10.])
    arctic, north_mlat, trop, south_mlat, ant=percentage_zonal_distrib_AT(long_AT,lat_AT)
    assert arctic==10.
    assert north_mlat==30.
    assert trop==40.
    assert south_mlat==10.
    assert ant==10.

def test_all_AT_pixels_are_in_the_tropics():
    lat_AT=np.array([ -20., 0., 15.,16.])
    long_AT=np.array([10.,10.,10.,10.])
    arctic, north_mlat, trop, south_mlat, ant=percentage_zonal_distrib_AT(long_AT,lat_AT)
    assert arctic==0.
    assert north_mlat==0.
    assert trop==100.
    assert south_mlat==0.
    assert ant==0.
    

    


    
    


    
    
    
    
    
    
    

