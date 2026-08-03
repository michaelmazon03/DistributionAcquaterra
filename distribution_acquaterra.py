#importo librerie
import os
import numpy as np
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.DEBUG)

#definizione directory e file
dir_home=os.getcwd()
dir_output=dir_home+"\\output"
dir_data=dir_home+"\\data"

if not(os.path.isdir(dir_output)):
    os.mkdir("output")



labels_time_step=["000.0","000.5","001.0","001.5","002.0","002.5","003.0","003.5","004.0","004.5",
                  "005.0","005.5","006.0","006.5","007.0","007.5","008.0","008.5","009.0","009.5",
                  "010.0","010.5","011.0","011.5","012.0","012.5","013.0","013.5","014.0","014.5",
                  "015.0","015.5","016.0","016.5","017.0","017.5","018.0","018.5","019.0","019.5",
                  "020.0","020.5","021.0","021.5","022.0","022.5","023.0","023.5","024.0","024.5",
                  "025.0","025.5","026.0"]

n_time_step=len(labels_time_step)

#value parameters

#Earth's parameters
earth_radius=6371.
R=100
n_total_pixels=40*R*(R-1)+12
area_pixels=(4*np.pi*earth_radius**2)/float(n_total_pixels)
earth_area=4.*np.pi*earth_radius**2.



def sort_coordinates(long,lat):
    """sort the 1D numpy arrays of coordinates (long=longitude and lat=latitudes), first by ascending latitutude,
    then by ascending longitude.
    """
    assert len(long)==len(lat), (
        f"Dimension of the longitudes={len(long)} and latitudes={len(lat)} numpy vectors are different;"
        f"since they are coupled, their dimensions must be equal."
    )
    
    n_coord=len(long)
    logging.debug("Sorting: number of pixels to be valuated="+str(n_coord)+ " ...")
    for i in range(n_coord):

        if i==int(n_coord/10.):
            logging.debug("[1/10] of the process. Sorted "+str(i)+" elements.")
        elif i==int(n_coord/10.*2.):
            logging.debug("[2/10] of the process. Sorted "+str(i)+" elements.")
        elif i==int(n_coord/10.*3.):
            logging.debug("[3/10] of the process. Sorted "+str(i)+" elements.")
        elif i==int(n_coord/10.*4.):
            logging.debug("[4/10] of the process. Sorted "+str(i)+" elements.")
        elif i==int(n_coord/10.*5.):
            logging.debug("[5/10] of the process. Sorted "+str(i)+" elements.")
        elif i==int(n_coord/10.*6.):
            logging.debug("[6/10] of the process. Sorted "+str(i)+" elements.")
        elif i==int(n_coord/10.*7.):
            logging.debug("[7/10] of the process. Sorted "+str(i)+" elements.")
        elif i==int(n_coord/10.*8.):
            logging.debug("[8/10] of the process. Sorted "+str(i)+" elements.")
        elif i==int(n_coord/10.*9.):
            logging.debug("[9/10] of the process. Sorted "+str(i)+" elements.")
            
        long_test=long[i]
        lat_test=lat[i]
        n_cycles=n_coord-i
        index_min=i
        for j in range(n_cycles):
            if lat_test>lat[i+j]:
                #if long_test>long[i+j]:
                lat_test=lat[i+j]
                long_test=long[i+j]
                index_min=i+j
            elif lat_test==lat[i+j] and long_test>long[i+j]:
                lat_test=lat[i+j]
                long_test=long[i+j]
                index_min=i+j

        lat[index_min]=lat[i]
        long[index_min]=long[i]
        lat[i]=lat_test
        long[i]=long_test

    logging.debug("Sorting complited")
    return long, lat


def sort_coordinates_lexsort(long,lat):
    """sort the 1D numpy arrays of coordinates (long=longitude and lat=latitudes), first by ascending latitutude,
    then by ascending longitude.
    """
    assert len(long)==len(lat), (
        f"Dimension of the longitudes={len(long)} and latitudes={len(lat)} numpy vectors are different;"
        f"since they are coupled, their dimensions must be equal."
    )
    
    
    indices=np.lexsort((long,lat))

    long[:]=long[indices]
    lat[:]=lat[indices]
    
    logging.debug("Sorting complited")
    return long, lat

def check_coordinates_are_sorted(long, lat):
    """check that the coordinate 1D arrays are already sorted according to the convention defined in the sort_coordinates function:
    the coordinates are sorted first by ascending latitutude, then by ascending longitude. The function returns a boolean value.
    """
    assert len(long)==len(lat), (f"Dimensions of the coupled vectors of longitudes = {len(start_long)}"
                                 f"and latitudes = {len(start_lat)} are different.")

    n_coord=len(long)
    arrays_are_sorted=True
    for i in range(n_coord-1):
        if lat[i]>lat[i+1]:
            arrays_are_sorted=False
        elif lat[i]==lat[i+1]:
            if long[i]>long[i+1]:
                arrays_are_sorted=False

    return arrays_are_sorted
        
                
        
def pixels_inundated(start_long, start_lat, end_long, end_lat):
    """given a pair of arrays (of longitudes and latitudes) of the pixels
    of an initial distribution (start_long and start_lat)  describing  the dry land (continent function) and those of a
    final distribution (end_long and end_lat), it returns the coordinate arrays of those pixels which disapear from the
    initial distribution to the final ditribution; in other words, the pixels which have been inundated. 
    """
    assert len(start_long)==len(start_lat), (f"Dimensions of the coupled vectors of starting longitudes = {len(start_long)}"
                                             f"and latitudes = {len(start_lat)} are different.")
    assert len(end_long)==len(end_lat), (f"Dimensios of the coupled vectors of final longitudes = {len(end_long)}"
                                             f"and latitudes = {len(end_lat)} are different.")

##    assert check_coordinates_are_sorted(start_long, start_lat), (f"The starting coordinate arrays (start_long and start_lat) are not sorted. The pixels_inundated"
##                                                                 f"works properly with both the initial and final coordinates arrays given in input"
##                                                                 f"which are properly  sorted  according to the convention defined in the"
##                                                                 f"sort_coordinate function")
##    assert check_coordinates_are_sorted(end_long, end_lat), (f"The final coordinate arrays (end_long and end_lat) are not sorted. The pixels_inundated"
##                                                             f"works properly with both the initial and final coordinates arrays given in input"
##                                                             f"which are properly  sorted  according to the convention defined in the"
##                                                             f"sort_coordinate function")
##
    
##    logging.debug("Sorting starts coordinates...")
##    sort_coordinates(start_long, start_lat)
##    logging.debug("Sorting end coordinates...")
##    sort_coordinates(end_long, end_lat)
    
    end_long_test=end_long
    end_lat_test=end_lat
    n_pixels_start=len(start_long)
    mask_pixels_inundated=[]

    logging.debug("Evaluating pixels inundated. Number of pixels to be valuated="+str(n_pixels_start)+ " ...")
    for j in range(n_pixels_start):
        if j==int(n_pixels_start/10.):
            logging.debug("[1/10] of the process. Analized "+str(j)+" elements.")
        elif j==int(n_pixels_start/10.*2.):
            logging.debug("[2/10] of the process. Analized "+str(j)+" elements.")
        elif j==int(n_pixels_start/10.*3.):
            logging.debug("[3/10] of the process. Analized "+str(j)+" elements.")
        elif j==int(n_pixels_start/10.*4.):
            logging.debug("[4/10] of the process. Analized "+str(j)+" elements.")
        elif j==int(n_pixels_start/10.*5.):
            logging.debug("[5/10] of the process. Analized "+str(j)+" elements.")
        elif j==int(n_pixels_start/10.*6.):
            logging.debug("[6/10] of the process. Analized "+str(j)+" elements.")
        elif j==int(n_pixels_start/10.*7.):
            logging.debug("[7/10] of the process. Analized "+str(j)+" elements.")
        elif j==int(n_pixels_start/10.*8.):
            logging.debug("[8/10] of the process. Analized "+str(j)+" elements.")
        elif j==int(n_pixels_start/10.*9.):
            logging.debug("[9/10] of the process. Analized "+str(j)+" elements.")
        
        pixel_has_been_inundated=True
        for i in range(len(end_long_test)):
            if start_long[j]==end_long_test[i] and start_lat[j]==end_lat_test[i]:
                pixel_has_been_inundated=False
                np.delete(end_long_test, range(0,i))
                np.delete(end_lat_test, range(0,i))
                break
        
        mask_pixels_inundated.append(pixel_has_been_inundated)

    assert len(mask_pixels_inundated)==len(start_long), (f"Mask vector = {len(mask_pixels_inundated)}"
                                                        f"must have the same dimension as the longitude vector = {len(start_lat)}"
                                                        f" to which it is applied.")
    lat_pixels_inundated=start_lat[mask_pixels_inundated]
    long_pixels_inundated=start_long[mask_pixels_inundated] 
    
    return long_pixels_inundated, lat_pixels_inundated

def pixels_inundated_setdiff1d(start_coordinates, end_coordinates):
    """given a pair of arrays (of longitudes and latitudes) of the pixels
    of an initial distribution (start_long and start_lat)  describing  the dry land (continent function) and those of a
    final distribution (end_long and end_lat), it returns the coordinate arrays of those pixels which disapear from the
    initial distribution to the final ditribution; in other words, the pixels which have been inundated. 
    """
    
##    assert check_coordinates_are_sorted(start_long, start_lat), (f"The starting coordinate arrays (start_long and start_lat) are not sorted. The pixels_inundated"
##                                                                 f"works properly with both the initial and final coordinates arrays given in input"
##                                                                 f"which are properly  sorted  according to the convention defined in the"
##                                                                 f"sort_coordinate function")
##    assert check_coordinates_are_sorted(end_long, end_lat), (f"The final coordinate arrays (end_long and end_lat) are not sorted. The pixels_inundated"
##                                                             f"works properly with both the initial and final coordinates arrays given in input"
##                                                             f"which are properly  sorted  according to the convention defined in the"
##                                                             f"sort_coordinate function")

    coord_pixels_inundated=np.setdiff1d(start_coordinates,end_coordinates)
    
    return coord_pixels_inundated
    


def determine_history_acquaterra(labels_time_step):
    
    return history_acquaterra

def regional_acquaterra(long_min, long_max, lat_min, lat_max, long_acquaterra, lat_acquaterra):
    """given a limited, rectangular region of on earth's surface indicated by the latitudes (lat_min and lat_max) and longitudes(long_min and long_max)
    limits and the global distribution of acquaterra, it returns the coordinate arrays of those acquaterranian pixels which are inside the given region
    """
    
    
    assert len(long_acquaterra)==len(lat_acquaterra), (f"Dimensions of the coupled vectors long_acquaterra = {len(long_acquaterra)}"
                                                       f"and lat_acquaterra = {len(lat_acquaterra)} are different.")
    assert lat_min<lat_max, (f"Minimum latitude = {lat_min} of the rectangular region "
                            f"must be smaller than maximum latitude ={lat_max}.")
    assert lat_min>=-90., (f"Minimum latitude= {lat_min} must be greater than or equal to -90"
                          f"Latitudes are defined between -90 and 90 degrees.")
    assert lat_min<90.,(f"Minimum latitude= {lat_min} must  be lower than 90."
                        f"Latitudes are defined between -90 and 90 degrees.")
    assert lat_max>-90., (f"Maximum latitude= {lat_max} must be greater than -90."
                          f"Latitudes are defined between -90 and 90 degrees.")
    assert lat_max<=90., (f"Maximum latitude= {lat_max} must be lower than or equal to 90."
                          f"Latitudes are defined between -90 and 90 degrees.")
    assert long_min>=0., (f"Minimum longitudes= {long_min} must be grater than or equal to 0 "
                          f"Longitudes are conventionally defined between 0 and 360 degrees.")
    assert long_min<=360., (f"Minimum longitudes= {long_min} must be lower than or equal to 360. "
                           f"Longitudes are conventionally defined between 0 and 360 degrees.")
    assert long_max>=0., (f"Maximunm longitudes= {long_max} must be grater than or equal to 0. "
                         f"Longitudes are conventionally defined between 0 and 360 degrees.")
    assert long_max<=360., (f"Maximunm longitudes= {long_max} must be lower than or equal to 360. "
                            f"Longitudes are conventionally defined between 0 and 360 degrees.")
    
    n_pixels_acquaterra=len(long_acquaterra)
    mask_region=[]
    
    pixel_is_in_the_reagion=False

    for i in range(n_pixels_acquaterra):
        pixel_is_in_the_reagion=False
        if long_min<long_max:
            if long_acquaterra[i]>long_min and long_acquaterra[i]<long_max:
                if lat_acquaterra[i]>lat_min and lat_acquaterra[i]<lat_max:
                    pixel_is_in_the_reagion=True
        elif long_max<long_min:
             if long_acquaterra[i]>long_min or long_acquaterra[i]<long_max:
                if lat_acquaterra[i]>lat_min and lat_acquaterra[i]<lat_max:
                    pixel_is_in_the_reagion=True
        mask_region.append(pixel_is_in_the_reagion)
    assert len(mask_region)==len(long_acquaterra), (f"Dimenstion Mask vector = {len(mask_region)}"
                                                    f"must be equal to the dimention of the  vectors = {len(long_acquaterra)}"
                                                    f" to which it is applied.")
    
    long_regional_acquaterra=long_acquaterra[mask_region]    
    lat_regional_acquaterra=lat_acquaterra[mask_region]
    
    return long_regional_acquaterra, lat_regional_acquaterra

def zonal_acquaterra(lat_min, lat_max, long_acquaterra, lat_acquaterra):
    """given a zonal region of on earth's surface indicated by the latitudes (lat_min and lat_max)
    limits and the global distribution of acquaterra, it returns the coordinate arrays of those
    acquaterranian pixels which are inside the given zonal region.
    """

    assert len(long_acquaterra)==len(lat_acquaterra), (f"Dimentions of the coupled vectors long_acquaterra = {len(long_acquaterra)}"
                                                       f"and lat_acquaterra = {len(lat_acquaterra)} are different.")
    assert lat_min<lat_max, (f"Minimum latitude = {lat_min} of the rectangular region "
                            f"must be smaller than maximum latitude ={lat_max}.")
    assert lat_min>=-90., (f"Minimum latitude= {lat_min} must be greater than or equal to -90"
                          f"Latitudes are defined between -90 and 90 degrees.")
    assert lat_min<90.,(f"Minimum latitude= {lat_min} must  be lower than 90."
                        f"Latitudes are defined between -90 and 90 degrees.")
    assert lat_max>-90., (f"Maximum latitude= {lat_max} must be greater than -90."
                          f"Latitudes are defined between -90 and 90 degrees.")
    assert lat_max<=90., (f"Maximum latitude= {lat_max} must be lower than or equal to 90."
                          f"Latitudes are defined between -90 and 90 degrees.")
    
    n_pixels_acquaterra=len(long_acquaterra)
    pixel_is_in_the_reagion=False
    mask_region=[]
    for i in range(n_pixels_acquaterra):
        pixel_is_in_the_reagion=False
        if lat_acquaterra[i]>lat_min and lat_acquaterra[i]<lat_max:
            pixel_is_in_the_reagion=True
        mask_region.append(pixel_is_in_the_reagion)
    lat_zonal_AT=lat_acquaterra[mask_region]
    long_zonal_AT=long_acquaterra[mask_region]
    return long_zonal_AT, lat_zonal_AT

def percentage_zonal_distrib_AT(long_acquaterra, lat_acquaterra):
    """given the coordinate arrays of the acquaterra distribution, it returns the percentages of the acquaterra ditribution inside some specific
    pre-defined zonal regions; specifically, they have  been  defined the arctic, northern mid-latitudes, tropics, southern mid-latitudes and antarctic regions.
    """
    assert len(long_acquaterra)==len(lat_acquaterra), (f"Dimentions of the coupled vectors long_acquaterra = {len(long_acquaterra)}"
                                                       f"and lat_acquaterra = {len(lat_acquaterra)} are different.")

    n_pixels_acquaterra=len(long_acquaterra)
    lat_max_arctic=90.
    lat_min_arctic=66.
    lat_max_north_mid_latitudes=66.
    lat_min_north_mid_latitudes=23.
    lat_max_tropics=23.
    lat_min_tropics=-23.
    lat_max_south_mid_latitudes=-23.
    lat_min_south_mid_latitudes=-66.
    lat_max_antarctic=-66.
    lat_min_antarctic=-90.

    logging.debug("computing acquaterra distribution on arctic")
    long_arctic, lat_arctic =zonal_acquaterra(lat_min_arctic, lat_max_arctic, long_acquaterra, lat_acquaterra)
    logging.debug("computing acquaterra distribution on northern mid latitude")
    long_north_mid_latitude, lat_north_mid_latitude =zonal_acquaterra(lat_min_north_mid_latitudes, lat_max_north_mid_latitudes,
                                                                      long_acquaterra, lat_acquaterra)
    logging.debug("computing acquaterra distribution on tropics")
    long_tropics, lat_tropics =zonal_acquaterra(lat_min_tropics, lat_max_tropics, long_acquaterra, lat_acquaterra)
    logging.debug("computing acquaterra distribution on southern mid latitude")
    long_south_mid_latitudes, lat_south_mid_latitudes =zonal_acquaterra(lat_min_south_mid_latitudes, lat_max_south_mid_latitudes,
                                                                        long_acquaterra, lat_acquaterra)
    logging.debug("computing acquaterra distribution on antarctic")
    long_antarctic, lat_antarctic =zonal_acquaterra(lat_min_antarctic, lat_max_antarctic, long_acquaterra, lat_acquaterra)

    
    perc_arctic=len(long_arctic)/n_pixels_acquaterra*100.
    assert perc_arctic>=0. and perc_arctic<=100., (f"perc_arctic ={perc_arctic} must be a percentage within 0 and 100%")
    perc_north_mid_lat=len(long_north_mid_latitude)/n_pixels_acquaterra*100.
    assert perc_north_mid_lat>=0. and perc_north_mid_lat<=100., (f"perc_north_mid_lat ={perc_north_mid_lat} must be a percentage within 0 and 100%")
    perc_tropics=len(long_tropics)/n_pixels_acquaterra*100.
    assert perc_tropics>=0. and perc_tropics<=100., (f"perc_tropics ={perc_tropics} must be a percentage within 0 and 100%")
    perc_south_mid_lat=len(long_south_mid_latitudes)/n_pixels_acquaterra*100.
    assert perc_south_mid_lat>=0. and perc_south_mid_lat<=100., (f"perc_south_mid_lat ={perc_south_mid_lat} must be a percentage within 0 and 100%")
    perc_antarctic=len(long_south_mid_latitudes)/n_pixels_acquaterra*100.
    assert perc_antarctic>=0. and perc_antarctic<=100., (f"perc_antarctic ={perc_antarctic} must be a percentage within 0 and 100%")

    return perc_arctic, perc_north_mid_lat, perc_tropics, perc_south_mid_lat, perc_antarctic


    
def mask_pixels_acquaterra(long_acquaterra, lat_acquaterra, long_global, lat_global):
    assert len(long_acquaterra)==len(lat_acquaterra), (f"Dimentions of the coupled vectors long_acquaterra = {len(long_acquaterra)}"
                                                       f"and lat_acquaterra = {len(lat_acquaterra)} are diffferent.")
    assert len(long_global)==len(lat_global), (f"Dimentions of the coupled vectors of the coordinates of every pixels of earth's surface"
                                               f"long_global = {len(long_global)}"
                                               f"and lat_global = {len(lat_global)} must be equal.")

    #sort_coordinates(long_acquaterra, lat_acquaterra)
    #sort_coordinates(long_global, lat_global)
    n_pixels_acquaterra=len(long_acquaterra)
    n_pixels_global=len(long_global)
    mask_pixels_acquaterra=[]

    j=0
    for i in range(n_pixels_global):
       # n_pixels_end=len(global_long_test)
        pixel_is_acquaterranian=False
        if j==n_pixels_acquaterra:
            pixel_is_acquaterranian=False
        elif long_acquaterra[j]==long_global[i] and lat_acquaterra[j]==lat_global[i]:
            pixel_is_acquaterranian=True
            j=j+1
        mask_pixels_acquaterra.append(pixel_is_acquaterranian)
    assert len(mask_pixels_acquaterra)==n_pixels_global, (f"Dimension of the mask mask_pixel_acquaterra = {len(mask_pixels_acquaterra)} "
                                                          f"is different to the number of pixels of the global pixelization of the Earth's surface = {n_pixels_global}")
    assert j==n_pixels_acquaterra, (f"Number of acquaterra pixels found in the sets of all pixels of earth's surface = {j} "
                                    f"is different to the number of pixels of the acquaterra distribution = {n_pixels_acquaterra}")
    return mask_pixels_acquaterra

def time_derevative_function(time_function, time_step):
    
    time_derevative=np.zeros(len(time_function))
    rec_den=1./time_step
    for i in range(len(time_function)):
        if i==0:
            time_derevative[i]=(time_function[i+1]-time_function[i])*rec_den
        elif i==len(time_function)-1:
            time_derevative[i]=(time_function[i]-time_function[i-1])*rec_den
        else:
            time_derevative[i]=((time_function[i]-time_function[i-1])*rec_den+(time_function[i+1]-time_function[i])*2.)*0.5
    return time_derevative

    
    

def read_file_coordinates_as_2d_array(file_name):
    os.chdir(dir_data)
    long=np.genfromtxt(file_name, comments='#', usecols=(0), dtype='f8')
    lat=np.genfromtxt(file_name, comments='#', usecols=(1), dtype='f8')
    n_coord=len(long)
    coord_2d_array=np.empty((n_coord,2))
    coord_2d_array[:,0]=long
    coord_2d_array[:,1]=lat
    return coord_2d_array

def read_file_coordinates(file_name):
    os.chdir(dir_data)
    long=np.genfromtxt(file_name, comments='#', usecols=(0), dtype='f8')
    lat=np.genfromtxt(file_name, comments='#', usecols=(1), dtype='f8')
    return long, lat

def read_file_field_on_earth_suf(file_name):
    os.chdir(dir_data)
    long=np.genfromtxt(file_name, comments='#', usecols=(0), dtype='f8')
    lat=np.genfromtxt(file_name, comments='#', usecols=(1), dtype='f8')
    field=np.genfromtxt(file_name, comments='#', usecols=(2), dtype='f8')
    
    return long, lat, field

def save_coord_distrib_as_txt_file(long_distrib, lat_distrib, file_name):
    assert len(long_distrib)==len(lat_distrib)
    os.chdir(dir_output)

    n_distrib=len(long_distrib)
    res=np.zeros(n_distrib, dtype=[("var1",float),("var2",float)])
    res["var1"]=long_distrib
    res["var2"]=lat_distrib
    f=open(file_name,"w")
    np.savetxt(f,res,delimiter="",fmt="%f\t %f\t", newline=os.linesep, header="longitude\t latitude\t\t")
    f.close()

    return

def save_plot_history_AT(history_AT,file_name):
    
    plt.figure(figsize=(10,6))
    time_step=np.arange(26,-0.5,-0.5)
    os.chdir(dir_plot)
    plt.xlim(26,0)
    plt.plot(time_step,history_AT, color="r", linestyle='-', lw=1, marker='o', markersize=3)
    plt.xlabel('year BP [kyr]', fontsize=15)
    plt.ylabel('Area acquaterra [km^2 * 10^3]', fontsize=15)
    plt.xticks(np.arange(26,-1,-2))
    plt.savefig(file_name, dpi=150)

    return


def save_plot_AT_time_derevative(AT_time_derevative,file_name):
    plt.figure(figsize=(10,6))
    time_step=np.arange(26,-0.5,-0.5)
    os.chdir(dir_plot)
    plt.xlim(26,0)
    plt.plot(time_step,time_derevative_AT, color="b", linestyle='-', lw=1, marker='o', markersize=3)
    plt.xlabel('year BP [kyr]', fontsize=15)
    plt.ylabel('AT area time derevative [km^2 * 10^3 / 500 yr]', fontsize=12)
    plt.xticks(np.arange(26,-1,-2))
    plt.axvspan(14.8,12.3, facecolor="#a2c4c9", alpha=0.3, edgecolor="black", linestyle="--", label="WMP-1a")
    plt.axvspan(11.5,8.8, facecolor="#a9c9a2", alpha=0.3, edgecolor="black", linestyle="--", label="WMP-1b"),   plt.legend(loc="lower right", fontsize=14)

    plt.savefig(file_name, dpi=150)

    return

    


def main():
    

    #Determination of acquaterra (AT) distributio
    logging.info("Compiuting distibution acquaterra...")
    file_CF_LGM="continent.026.0.dat"
    file_CF_present_day="continent.000.0.dat"

    
    long_CF_LGM, lat_CF_LGM= read_file_coordinates(file_CF_LGM)
    long_CF_present_day, lat_CF_present_day= read_file_coordinates(file_CF_present_day)
    sort_coordinates_lexsort(long_CF_LGM, lat_CF_LGM)
    sort_coordinates_lexsort(long_CF_present_day, lat_CF_present_day)
    long_acquaterra, lat_acquaterra=pixels_inundated(long_CF_LGM,
                                                     lat_CF_LGM,
                                                     long_CF_present_day,
                                                     lat_CF_present_day)
    #Save the output

    logging.info("Saving output acquaterra distribution...")
    file_name="distribution_acquaeterra.dat"
    save_coord_distrib_as_txt_file(long_acquaterra, lat_acquaterra, file_name)


    #STATISTICS ACQUATERRA

    logging.info("Computing some statistics of acquaterra distribution...")

    #area acquaterra
    n_pixels_AT=len(long_acquaterra)
    area_AT=n_pixels_AT*area_pixels

    
    #MEAN SEA-LEVEL on acquaterra (AT)
    #reading file topography
    file_name='topo.000.0.dat'
    long_global, lat_global, topography= read_file_field_on_earth_suf(file_name)
    sea_level=topography*1.
    logging.info("Computing mean sea level on acquaterra")
    sort_coordinates_lexsort(long_acquaterra, lat_acquaterra)
    mask_sea_level_AT=mask_pixels_acquaterra(long_acquaterra, lat_acquaterra, long_global, lat_global)
    sea_level_AT=sea_level[mask_sea_level_AT]
    mean_SL_AT=np.mean(sea_level_AT)

    #REGIONAL ACQUATERRA
    #longitudes and latitudes limits of mediterranean sea
    des_region="Mediterranean sea"
    reg_long_min=354.
    reg_long_max=36.
    reg_lat_min=30.
    reg_lat_max=46.

    logging.info("Computing distribution acquaterra in "+des_region)
    reg_long_AT, reg_lat_AT=regional_acquaterra(reg_long_min,
                                                reg_long_max,
                                                reg_lat_min,
                                                reg_lat_max,
                                                long_acquaterra,
                                                lat_acquaterra)
    
    #Save the output
                           
    logging.debug("Saving output distribution acquaterra in "+des_region)
    file_name="distribution_AT_mediterranean_sea.dat"
    save_coord_distrib_as_txt_file(reg_long_AT, reg_lat_AT, file_name)

    #area regional acquaterra

    n_pixels_reg_AT=len(reg_long_AT)
    area_reg_AT=n_pixels_reg_AT*area_pixels

    #mean sea level on regional acquaterra
    #reading file topography
    file_name='topo.000.0.dat'
    long_global, lat_global, topography= read_file_field_on_earth_suf(file_name)
    sea_level=topography*1.
    logging.info("Computing mean sea level on the regional acquaterra:" +des_region)
    mask_sl_reg_AT=mask_pixels_acquaterra(reg_long_AT, reg_lat_AT, long_global, lat_global)
    sea_level_reg_AT=sea_level[mask_sl_reg_AT]
    mean_SL_reg_AT=np.mean(sea_level_reg_AT)

    #zonal ditribution acquaterra
    logging.info("Computing zonal distribution acquaterra")
    perc_arctic, perc_north_mid_lat, perc_trop, perc_south_mid_lat, perc_ant= percentage_zonal_distrib_AT(long_acquaterra, lat_acquaterra)

    #save statistics
                           
    name_file="statistics_acquaterra.dat"
    logging.debug("Saving statistics on file "+namefile+"...")
    
    statistics=np.array([area_AT, mean_SL_AT, area_reg_AT, mean_SL_reg_AT,
                         perc_arctic, perc_north_mid_lat, perc_trop, perc_south_mid_lat, perc_ant])
    description=np.array(["Area acquaterra [m^2]",
                         "Mean sea-level [m]",
                         "Area acquaterra "+des_region+" [m^2]",
                         "Mean sea-level"+des_region+" [m]",
                         "Percentage AT in arctic  [%]",
                         "Percentage AT in northern mid latiudes  [%]",
                         "Percentage AT in tropics  [%]",
                         "Percentage AT in southern mid latitudes  [%]",
                         "Percentage AT in antarctic  [%]"])
    n_row=len(statistics)
    res=np.zeros(n_row, dtype=[("var1",str),("var2",float)])
    res["var1"]=description
    res["var2"]=statistics
    f=open(name_file,"w")
    np.savetxt(f,res,delimiter="",fmt="%s\t %f\t", newline=os.linesep, header="description\t value\t\t")
    f.close()
    


    
    
    
    #Determination history acquaterra
    logging.info("Computing time history of acquaterra")
    n_pixels_history_AT=np.zeros(n_time_step)
    for j in range(n_time_step):
        #logging.debug("Computing distribution acquaterra at epoch "+labels_time_step[j]+" kyr BP")
        file_name="continent."+labels_time_step[j]+".dat"
        long_CF_current, lat_CF_current= read_file_coordinates(file_name)

        long_AT_current, lat_AT_current=pixels_inundated(long_acquaterra,
                                                         lat_acquaterra,
                                                         long_AT_current,
                                                         lat_AT_current)
            
        
        file_name="coordinates_acquaterra"+labels_time_step[j]
        save_coord_distrib_as_txt_file(long_AT_current, lat_AT_current, file_name)
        n_pixels_history_AT[j]=len(long_AT_current)

    history_acquaterra=n_pixels_history_AT/n_tot_pixel*100.
    history_acquaterra=np.flip(history_acquaterra)
    history_acquaterra=history_acquaterra*area_pixel*0.01*10**(-3.)

    time_step=0.5
    time_derevative_AT=time_derevative_function(history_acquaterra, time_step)

    

    #plot
    logging.info("Producing graph of the history of acquaterra and its time derevative;and saving the"
                 "figures...")
    
    file_name='graph_evolution_acquaterra_area.png'
    save_plot_history_AT(history_acquaterra,file_name)
    file_name='graph_AT_area_time_derivative.png'
    save_plot_AT_time_derevative(AT_time_derevative,file_name)

    return


    


if __name__=="__main__":
    main()
