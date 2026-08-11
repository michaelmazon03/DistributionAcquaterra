#file test.py
from distribution_acquaterra import (sort_coordinates,
                                     sort_coordinates_lexsort,
                                     check_coordinates_are_sorted,
                                     pixels_inundated,
                                     pixels_not_inundated,
                                     regional_acquaterra,
                                     mask_pixels_acquaterra,
                                     zonal_acquaterra,
                                     percentage_zonal_distrib_AT,
                                     main)
import numpy as np
import pytest
from pathlib import Path




###########################################

def test_sorting_lat_is_correct():

    """this function tests that the sort_coordinates function
    sort the sequenze of coordinates long and lat first by ascending latitutude,
    then by ascending longitude.

    GIVEN: proper list of latitude and longitude
    WHEN: I apply to the list the sort_coordinates function
    THEN: the list of coordinates will be sorted by ascending
    latitude and longitude
    """
    long=[250., 300., 280.]
    lat=[30., -30.5, 20.5]
    sort_coordinates(long,lat)

    assert [long, lat]==[[300., 280., 250.],[-30.5, 20.5, 30.]]
    assert [long, lat]!=[[250., 300., 280.],[30., -30.5, 20.5]]

def test_sorting_long_is_correct():
    """this function tests that the sort_coordinates function
    sort properly the longitudes in ascnding order.

    GIVEN:  list of latitudes of the same value and a list of longitudes
    randomly ordered
    WHEN: the sort_coordinates function is applied to the lists of longitude
    and latitude
    THEN: the list of coordinates will be sorted by ascending
    longitude
    """
    long=[250., 300., 280.]
    lat=[30., 30., 30.]
    sort_coordinates(long,lat)

    assert [long, lat]==[[250., 280., 300.],[30., 30., 30.]]
    assert [long, lat]!=[[250., 300., 280.],[30., -30.5, 20.5]]

def test_sorting_latitudes_already_sorted():
    """this function tests that the sort_coordinates function gives the initial
    lists of longitudes and latitudes if those are already sorted.

    GIVEN:  lists latitude already
    sorted and a list of longitude of the same value
    WHEN: the sort_coordinates function is applied to the lists
    THEN: the lists remain unchanged
    """
    initial_lat=[10., 20., 30.]
    initial_long=[10.,10.,10.]
    sort_coordinates(initial_long,initial_lat)
    
    assert [initial_long, initial_lat]==[[10.,10.,10.], [10., 20., 30.]]

def test_sorting_longitudes_already_sorted():
    """this function tests that the sort_coordinates function gives the initial
    lists if the logitudes  are already sorted and latitudes are all identical.

    GIVEN:  lists longitudes already sorted and a list of latitudes
    of the same value
    WHEN: the sort_coordinates function is applied to the lists 
    THEN: the lists remain unchanged
    """
    initial_lat=[10.,10.,10.]
    initial_long=[100.,200.,300.]
    
    lat_var=initial_lat
    long_var=initial_long
    sort_coordinates(long_var,lat_var)

    assert [long_var, lat_var]==[initial_long, initial_lat]

def test_sorting_with_nplexsort_lat_is_correct():

    """this function tests that the sort_coordinates_lexsort function
    sort the   coordinates numpy arrays long and lat first by ascending latitutude,
    then by ascending longitude.

    GIVEN: proper list of latitude and longitude
    WHEN: I apply to the list the sort_coordinates function
    THEN: the list of coordinates will be sorted by ascending
    latitude and longitude
    """
    long=np.array([250., 300., 280.])
    lat=np.array([30., -30.5, 20.5])
    sort_coordinates_lexsort(long,lat)

    assert np.array_equal(long,np.array([300., 280., 250.]))
    assert np.array_equal(lat,np.array([-30.5, 20.5, 30.]))

def test_sorting_with_nplexsort_long_is_correct():
    """this function tests that the sort_coordinates_lexsort function
    sort properly the longitudes in ascnding order.

    GIVEN:  list of latitudes of the same value and a list of longitudes
    randomly ordered
    WHEN: the sort_coordinates function is applied to the lists of longitude
    and latitude
    THEN: the list of coordinates will be sorted by ascending
    longitude
    """
    long=np.array([250., 300., 280.])
    lat=np.array([30., 30., 30.])
    sort_coordinates_lexsort(long,lat)

    assert np.array_equal(long,np.array([250., 280., 300.]))
    assert np.array_equal(lat,np.array([30., 30., 30.]))

def test_sorting_with_nplexsort_latitudes_already_sorted():
    """this function tests that the sort_coordinates_lexsort function gives the initial
    arrays  of longitudes and latitudes  if those are already sorted.

    GIVEN:  lists latitude already
    sorted and a list of longitude of the same value
    WHEN: the sort_coordinates function is applied to the lists
    THEN: the lists remain unchanged
    """
    initial_lat=np.array([10., 20., 30.])
    initial_long=np.array([10.,10.,10])
    sort_coordinates_lexsort(initial_long,initial_lat)

    assert np.array_equal(initial_long,np.array([10.,10.,10.]))
    assert np.array_equal(initial_lat,np.array([10., 20., 30.]))

def test_sorting_with_nplexsort_longitudes_already_sorted():
    """this function tests that the sort_coordinates_lexsort function gives the initial
    arrays if the logitudes  are already sorted and latitudes are all identical.

    GIVEN:  lists longitudes already sorted and a list of latitudes
    of the same value
    WHEN: the sort_coordinates function is applied to the lists 
    THEN: the lists remain unchanged
    """
    initial_lat=np.array([10.,10.,10.])
    initial_long=np.array([100.,200.,300.])
    
    lat_var=initial_lat.copy()
    long_var=initial_long.copy()
    sort_coordinates_lexsort(long_var,lat_var)

    assert np.array_equal(long_var,initial_long)
    assert np.array_equal(lat_var,initial_lat)
    
def test_determination_pixels_inundated_is_correct():
    """this function tests that the pixels_inundated function works.

    GIVEN:  a pair of arrays (of longitudes and latitudes) of the pixels
    of an initial distribution (ideally, of the dry land) and those of a
    final distribution
    WHEN: the pixels_inundated function is applied to the arrays of
    initial and final distributions  
    THEN: the function returns a arrays of longitudes and latitudes of those pixels
    that have disappeared from the initial ditribution to the final distribution;
    
    """
    
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
    """this function tests  the limit case in which all the pixels
    were inundated.

    GIVEN:  the arrays (longitudes and latitudes) of the two distributions
    do not have any pixels in common.
    WHEN: the pixels_inundated function is applied to the arrays of
    initial and final distributions  
    THEN: the function returns arrays that are identical to the initial arrays
    """
    initial_lat=np.array([-20.,-10.,10.,20.])
    initial_long=np.array([0.,0.,0.,0.,])
    end_lat=np.array([10.])
    end_long=np.array([10.])
    long_inundated, lat_inundated=pixels_inundated(initial_long, initial_lat,
                                                  end_long, end_lat)

    assert len(long_inundated)==4

def test_no_pixels_have_been_inundated():
    """this function tests  the limit case in which no pixels
    were inundated.

    GIVEN:  the arrays (longitudes and latitudes) of the two distributions
    are identical.
    WHEN: the pixels_inundated function is applied to the arrays of
    initial and final distributions  
    THEN: the function returns arrays of length zero.
    """
    common_lat=[-20.,-10.,10.,20.]
    common_long=[0.,0.,0.,0.,]
    initial_lat=np.array(common_lat)
    initial_long=np.array(common_long)
    end_lat=np.array(common_lat)
    end_long=np.array(common_long)
    long_inundated, lat_inundated=pixels_inundated(initial_long, initial_lat,
                                                  end_long, end_lat)

    assert len(long_inundated)==0

def test_pixels_not_inundated_func_partial_inund():
    """this function tests that the pixels_not_inundated function works.

    GIVEN:  a pair of arrays (of longitudes and latitudes) of the pixels
    of an initial distribution (ideally, of the dry land) and those of a
    final distribution
    WHEN: the pixels_not_inundated function is applied to the arrays of
    initial and final distributions  
    THEN: the function returns a arrays of longitudes and latitudes of those pixels
    that have remained unalterated from the initial ditribution to the final distribution;
    
    """
    
    common_long=[100.,100.]
    common_lat=[10.,20.]
    diff_long=[150.]
    diff_lat=[10.]
    initial_long=np.concatenate((common_long, diff_long))
    initial_lat=np.concatenate((common_lat, diff_lat))
    end_long=np.array(common_long)
    end_lat=np.array(common_lat)
    long_not_inund, lat_not_inund=pixels_not_inundated(initial_long, initial_lat,
                                                  end_long, end_lat)

    assert len(long_not_inund)==2
    assert len(lat_not_inund)==2
    assert np.array_equal(long_not_inund,np.array(common_long))
    assert np.array_equal(lat_not_inund,np.array(common_lat))
    
def test_pixels_not_inundated_func_all_pixs_inund():
    """this function tests that the pixels_not_inundated function in
    the case all pixels have been inundated.

    GIVEN:  a pair of arrays (of longitudes and latitudes) of the pixels
    of an initial distribution (ideally, of the dry land) and those of a
    final distribution without coordinate elements in common.
    WHEN: the pixels_not_inundated function is applied to the arrays of
    initial and final distributions  
    THEN: the function returns an empty arrays of longitudes and latitudes
    """
    
    initial_long=np.array([10.,10.,10.,10.,10.])
    initial_lat=np.array([10.,20.,30.,40.,50.])
    end_long=np.array([10.])
    end_lat=np.array([60.])
    long_not_inund, lat_not_inund=pixels_not_inundated(initial_long, initial_lat,
                                                  end_long, end_lat)
    assert len(long_not_inund)==0
    assert len(lat_not_inund)==0
    
def test_pixels_not_inundated_func_no_pixs_inund():
    """this function tests that the pixels_not_inundated function in
    the case of no pixels have been inundated.

    GIVEN:  a pair of  arrays (of longitudes and latitudes) of the pixels
    of an initial distribution (ideally, of the dry land) and those of a
    final distribution, in which the initial distib is a subset of the fine one.
    WHEN: the pixels_not_inundated function is applied to the arrays of
    initial and final distributions  
    THEN: the function returns the arrays of longitudes and latitudes of the
    initaial distribution
    """
    long_common=[10.,10.,10.,10.,10.]
    lat_common=[10.,20.,30.,40.,50.]
    
    initial_long=np.array(long_common)
    initial_lat=np.array(lat_common)
    end_long=np.concatenate((long_common, [10.]))
    end_lat=np.concatenate((lat_common, [60.]))
    long_not_inund, lat_not_inund=pixels_not_inundated(initial_long, initial_lat,
                                                  end_long, end_lat)

    assert len(long_not_inund)==len(long_common)
    assert len(lat_not_inund)==len(lat_common)
    assert np.array_equal(long_not_inund, initial_long)
    assert np.array_equal(lat_not_inund, initial_lat)

def test_regional_acquaterra_works():
    """this function tests that the regional_acquaterra works properly.

    GIVEN:  the latitudes and longitudes limits of a given region and the
    acquaterra (AT) distribution (that is, the arrays of latitudes and longitudes
    of AT.
    WHEN: the regional_acquaeterra is applied
    THEN: the function returns the AT distribution enclosed within the given
    region.
    """
    lat_AT=np.array([10.,50.])
    long_AT=np.array([20.,20.])
    lat_min_reg=5.
    lat_max_reg=15.
    long_min_reg=15.
    long_max_reg=25.

    long_regional, lat_regional=regional_acquaterra(long_min_reg, long_max_reg,
                                                    lat_min_reg, lat_max_reg,
                                                    long_AT, lat_AT)

    assert len(lat_regional)==1 and len(long_regional)==1
    assert lat_regional[0]==10. and long_regional[0]==20.
    

def test_longitude_on_regional_AT():
    """this function tests that the regional_acquaterra works also in the special
    case in which the region studied includes the longitude =0; that is,
    the left border, in terms of longitude in degrees, is greater than the
    right border. (remmnber that longitude is conventionally defined between 0 and 360
    degrees).

    GIVEN:  a region that contains the longitude=0 and a
    certain distribution of AT with one element inside
    the region with longitude>0.
    WHEN: the regional_acquaeterra is applied
    THEN: the function returns the AT distribution enclosed within the given
    region.
    """

    lat_AT=np.array([10.,50.])
    long_AT=np.array([1.,20.])
    lat_min_reg=5.
    lat_max_reg=15.
    long_min_reg=355.
    long_max_reg=5.

    long_regional, lat_regional=regional_acquaterra(long_min_reg, long_max_reg,
                                                    lat_min_reg, lat_max_reg,
                                                    long_AT, lat_AT)

    assert len(lat_regional)==1 and len(long_regional)==1
    assert lat_regional[0]==10. and long_regional[0]==1.
    
def test_longitude_smaller_than_360_on_region():
    """this function tests the case of the region that include longitude=0,
    but consider a AT pixel within the region and with longitude <360.

    GIVEN:  a region that contain the longitude=0 and a
    certain distribution of AT with one element inside
    the region with longitude<360.
    WHEN: the regional_acquaeterra is applied
    THEN: the function returns the AT distribution enclosed within the given
    region.
    """

    lat_AT=np.array([10.,50.])
    long_AT=np.array([-1.,20.])
    lat_min_reg=5.
    lat_max_reg=15.
    long_min_reg=355.
    long_max_reg=5.

    long_regional, lat_regional=regional_acquaterra(long_min_reg, long_max_reg,
                                                    lat_min_reg, lat_max_reg,
                                                    long_AT, lat_AT)

    assert len(lat_regional)==1 and len(long_regional)==1
    assert lat_regional[0]==10. and long_regional==-1.

    
def test_lat_border_region_is_not_included():
    """this function tests the fact that the regioal_acquaeterra function
    has been designed  not to include the limits of the defined region.

    GIVEN:  a generic region of the earth's surface and an AT distribution
    with one pixel on the LATITUDIANAL border of the given region and one
    pixel outside.
    WHEN: the regional_acquaeterra is applied
    THEN: the function returns  empty arrays.
    """
    lat_AT=np.array([5.,50.])
    long_AT=np.array([20.,20.])
    lat_min_reg=5.
    lat_max_reg=15.
    long_min_reg=15.
    long_max_reg=25.

    long_regional, lat_regional=regional_acquaterra(long_min_reg, long_max_reg,
                                                    lat_min_reg, lat_max_reg,
                                                    long_AT, lat_AT)

    assert len(lat_regional)==0 and len(long_regional)==0

def test_long_border_region_is_not_included():
    """this function tests the fact that the regioal_acquaeterra function
    has been designed  not to include the limits of the defined region.

    GIVEN:  a generic region of the earth's surface and an AT distribution
    with one pixel on the LONGITUDINAL border of the given region and one
    pixel outside.
    WHEN: the regional_acquaeterra is applied
    THEN: the function returns  empty arrays.
    """
    lat_AT=np.array([10.,50.])
    long_AT=np.array([15.,20.])
    lat_min_reg=5.
    lat_max_reg=15.
    long_min_reg=15.
    long_max_reg=25.

    long_regional, lat_regional=regional_acquaterra(long_min_reg, long_max_reg,
                                                    lat_min_reg, lat_max_reg,
                                                    long_AT, lat_AT)

    assert len(lat_regional)==0 and len(long_regional)==0.
    
def test_mask_acquaterra_works():
    """this function tests the general behavior of the
    mask_pixel_acquaterra function.
    
    GIVEN:  arrays  of coordinates (longitude and latitudes). Ideally,
    they should represent all the pixels obtained by a proper pixelization
    of earth's surface but for this test we consider just a bunch of coordinates.
    Moreover, we have the coordinate arrays (based on the same pixelization)
    of the AT distribution.
    WHEN: the mask_pixel_acquaterra is applied
    THEN: the function returns a list of True and False with the same length as
    the global coordinates arrays; a True value is supposed to be in the indices
    corresponding to coordintes in which the AT distribution is present.
    """

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
    """this function tests the general behavior of the
    zonal_acquaeterra function.
    
    GIVEN:  the coordinate arrays of the AT distribution and a zonal
    region delimited by two limit latitudes.
    WHEN: the zonal_acquaeterra is applied
    THEN: returns a coordinates array of the AT pixels inside the given
    zonal region.
    """
    lat_AT=np.array([-85., -60., 0., 15., 30., 50., 80.])
    long_AT=np.array([10.,10.,10.,10.,10.,10.,10.])
    lat_min=-20.
    lat_max=40.
    long_reg, lat_reg=zonal_acquaterra(lat_min, lat_max, long_AT, lat_AT)
    assert len(long_reg)==3
    assert long_reg[0]==10. and lat_reg[0]==0.
    assert long_reg[1]==10. and lat_reg[1]==15.
    assert long_reg[2]==10. and lat_reg[2]==30.

def test_no_AT_pixels_in_zonal_region():
    """this function tests the zonal_acquaterra function in the case of no
    pixels of AT distribution are inside the azonal region.
    
    GIVEN:  the coordinate arrays of the AT distribution and a zonal
    region delimited by two limit latitudes.
    WHEN: the zonal_acquaeerra is applied
    THEN: the function returns  empty coordinate array.
    """
    lat_AT=np.array([-85., -60., -20., 0., 15., 30., 50., 80.])
    long_AT=np.array([10.,10.,10.,10.,10.,10.,10.,10.])
    lat_min=-10.
    lat_max=-5.
    long_reg, lat_reg=zonal_acquaterra(lat_min, lat_max, long_AT, lat_AT)
    assert len(long_reg)==0


def test_all_AT_pixels_are_in_the_zonal_reg():
    """this function tests the zonal_acquaterra function in the case where all
    pixels of AT distribution are inside the zonal region.
    
    GIVEN:  the coordinate arrays of the AT distribution and a zonal
    region delimited by two limit latitudes.
    WHEN: the zonal_acquaeerra is applied
    THEN: the function returns   coordinate arrays which are identical to the
    coordinate arrays of AT distribution given in input.
    """
    lat_AT=np.array([ -60., -20., 0., 15., 30., 50.])
    long_AT=np.array([10.,10.,10.,10.,10.,10.])
    lat_min=-65.
    lat_max=60.
    long_reg, lat_reg=zonal_acquaterra(lat_min, lat_max, long_AT, lat_AT)
    assert len(long_reg)==6
    assert long_reg.all()==long_AT.all() and lat_reg.all()==lat_AT.all()

def test_latitude_limits_are_not_included():
    """this function tests the fact that the zonal_acquaterra function
    has been designed  not to include the latitude limits of the defined
    zonal region.

    GIVEN:  a zonal region of the earth's surface and an AT distribution
    with one pixel on a latitudinal border of the given region.
    WHEN: the zonal_acquaterra is applied
    THEN: the function returns  the coordinate arrays of the AT distribution
    inside the zonal region under study, excluding the pixel on the border.
    """
    lat_AT=np.array([ -20., 0., 15., 30., 40.])
    long_AT=np.array([10.,10.,10.,10.,10.])
    lat_min=-20.
    lat_max=40.
    long_reg, lat_reg=zonal_acquaterra(lat_min, lat_max, long_AT, lat_AT)
    assert len(long_reg)==3
    assert long_reg[0]==10. and lat_reg[0]==0.
    assert long_reg[1]==10. and lat_reg[1]==15.
    assert long_reg[2]==10. and lat_reg[2]==30.


def test_percentage_zonal_distrib_AT_works():
    """this function tests the general behavior of the percentage_zonal_distrib_AT
    function.

    GIVEN: the coordinate arrays of the AT distribution.
    WHEN: the percentage_zonal_distrib_AT is applied
    THEN: the function retnurns  the percentages of pixels inside  each zonal
    region (arctic, norther mid-latitude etc.) defined inside the function.
    """
    lat_AT=np.array([-85., -60., -20., 0., 15.,16., 30., 50.,55., 80.])
    long_AT=np.array([10.,10.,10.,10.,10.,10.,10.,10.,10.,10.])
    arctic, north_mlat, trop, south_mlat, ant=percentage_zonal_distrib_AT(long_AT,lat_AT)
    assert arctic==10.
    assert north_mlat==30.
    assert trop==40.
    assert south_mlat==10.
    assert ant==10.

def test_all_AT_pixels_are_in_the_tropics():
    """this function tests the  percentage_zonal_distrib_AT
    function in the special case in which all the pixels are inside a single
    zonal region.

    GIVEN:  the coordinate arrays of the AT distribution describing pixels
    in the tropics region.
    WHEN: the percentage_zonal_distrib_AT is applied
    THEN: the function returns  100 percent for the tropics region and zero
    otherwise
    """
    lat_AT=np.array([ -20., 0., 15.,16.])
    long_AT=np.array([10.,10.,10.,10.])
    arctic, north_mlat, trop, south_mlat, ant=percentage_zonal_distrib_AT(long_AT,lat_AT)
    assert arctic==0.
    assert north_mlat==0.
    assert trop==100.
    assert south_mlat==0.
    assert ant==0.

def test_check_latitudes_are_sorted():
    """this tests the check_coordinates_are_sorted function for the latitudes.

    GIVEN:  the coordinate arrays (longitude and latitude) with the latitudes 
    sorted.
    WHEN: the check_coordinates_are_sorted function is applied
    THEN: the function returns  the boolean value True
    """

    long=np.array([10., 10., 10.])
    lat=np.array([10., 20., 30.])

    assert check_coordinates_are_sorted(long, lat)

def test_check_latitudes_are_not_sorted():
    """this tests the check_coordinates_are_sorted function for the latitudes.

    GIVEN:  the coordinate arrays (longitude and latitude) with the latitudes
    not sorted.
    WHEN: the check_coordinates_are_sorted function is applied
    THEN: the function returns  the boolean value False
    """

    long=np.array([10., 10.,10.])
    lat=np.array([20., 10., 30.])

    assert not check_coordinates_are_sorted(long, lat)

def test_check_longitudes_are_sorted():
    """this tests the check_coordinates_are_sorted function for the longitudes.

    GIVEN:  the coordinate arrays (longitude and latitude) with the longitude already
    sorted and latitudes wirh the same value.
    WHEN: the check_coordinates_are_sorted function is applied
    THEN: the function returns  the boolean value True
    """

    long=np.array([10., 20.,30.])
    lat=np.array([10., 10.,10.])

    assert check_coordinates_are_sorted(long, lat)

def test_check_longitudes_are_not_sorted():
    """this tests the check_coordinates_are_sorted function for the longitudes.

    GIVEN:  the coordinate arrays (longitude and latitude) with the longitudes 
    not sorted. 
    WHEN: the check_coordinates_are_sorted function is applied
    THEN: the function returns  the boolean value False
    """

    long=np.array([10., 5.,15.])
    lat=np.array([10., 10.,10.])

    assert not check_coordinates_are_sorted(long, lat)

def test_output_txt_files_have_been_created():
    dir_home=Path.cwd()
    dir_output=dir_home / 'output'
    path_distrib_acquaterra= dir_output / "distribution_acquaterra.dat"
    path_regional_AT= dir_output / "distribution_AT_mediterranean_sea.dat"
    path_statistics= dir_output / "statistics_acquaterra.dat"
    main()
    assert path_distrib_acquaterra.exists()
    assert path_regional_AT.exists()
    assert path_statistics.exists()

    

    

    


    
    


    
    
    
    
    
    
    

