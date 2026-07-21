#importo librerie
import os
import numpy as np
import matplotlib.pyplot as plt

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
area_pixel=(4*np.pi*earth_radius**2)/float(n_total_pixels)
earth_area=4.*np.pi*earth_radius**2.



def sort_coordinates(long,lat):
    n_coord=len(long)
    for i in range(n_coord):
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
    return long, lat
                
        
def pixels_inundated(start_long, start_lat, end_long, end_lat):
    assert len(start_long)==len(start_lat)
    assert len(end_long)==len(end_lat)
    sort_coordinates(start_long, start_lat)
    sort_coordinates(end_long, end_lat)
    end_long_test=end_long
    end_lat_test=end_lat
    n_pixels_start=len(start_long)
    mask_pixels_inundated=[]
    for j in range(n_pixels_start):
        pixel_has_been_inundated=True
        n_pixels_end=len(end_long_test)
        for i in range(len(end_long_test)):
            if start_long[j]==end_long_test[i] and start_lat[j]==end_lat_test[i]:
                pixel_has_been_inundated=False
                np.delete(end_long_test, range(0,i))
                np.delete(end_lat_test, range(0,i))
                break
        
        mask_pixels_inundated.append(pixel_has_been_inundated)
    lat_pixels_inundated=start_lat[mask_pixels_inundated]
    long_pixels_inundated=start_long[mask_pixels_inundated]
    
    return long_pixels_inundated, lat_pixels_inundated
    
def determine_distrib_acquaterra(long_lgm, lat_lgm, long_present_day, lat_present_day):
    long_acquaterra, lat_acquaterra=pixels_inundated(long_lgm, lat_lgm, long_present_day_lat(present_day))

    return long_acquaterra, lat_acquaterra

def determine_history_acquaterra(labels_time_step):
    
    return history_acquaterra

def regional_acquaterra(long_min, long_max, lat_min, lat_max, long_acquaterra, lat_acquaterra):
    assert len(long_acquaterra)==len(lat_acquaterra)
    assert lat_min<lat_max
    assert lat_min>=-90. and lat_min<90.
    assert lat_max>-90. and lat_max<=90.
    assert long_min>=0. and long_min<=360.
    assert lat_max>=0. and lat_max<=360.
    
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
    

    long_regional_acquaterra=long_acquaterra[mask_region]    
    lat_regional_acquaterra=lat_acquaterra[mask_region]
    
    return long_regional_acquaterra, lat_regional_acquaterra

def zonal_acquaterra(lat_min, lat_max, long_acquaterra, lat_acquaterra):
    assert len(long_acquaterra)==len(lat_acquaterra)
    assert lat_min<lat_max
    assert lat_min>=-90. and lat_min<90.
    assert lat_max>-90. and lat_max<=90.
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
    assert len(long_acquaterra)==len(lat_acquaterra)
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
    long_arctic, lat_arctic =zonal_acquaterra(lat_min_arctic, lat_max_arctic, long_acquaterra, lat_acquaterra)
    long_north_mid_latitude, lat_north_mid_latitude =zonal_acquaterra(lat_min_north_mid_latitudes, lat_max_north_mid_latitudes,
                                                                      long_acquaterra, lat_acquaterra)
    long_tropics, lat_tropics =zonal_acquaterra(lat_min_tropics, lat_max_tropics, long_acquaterra, lat_acquaterra)
    long_south_mid_latitudes, lat_south_mid_latitudes =zonal_acquaterra(lat_min_south_mid_latitudes, lat_max_south_mid_latitudes,
                                                                        long_acquaterra, lat_acquaterra)
    long_antarctic, lat_antarctic =zonal_acquaterra(lat_min_antarctic, lat_max_antarctic, long_acquaterra, lat_acquaterra)
    
    perc_arctic=len(long_arctic)/n_pixels_acquaterra*100.
    perc_north_mid_lat=len(long_north_mid_latitude)/n_pixels_acquaterra*100.
    perc_tropics=len(long_tropics)/n_pixels_acquaterra*100.
    perc_south_mid_lat=len(long_south_mid_latitudes)/n_pixels_acquaterra*100.
    perc_antarctic=len(long_south_mid_latitudes)/n_pixels_acquaterra*100.

    return perc_arctic, perc_north_mid_lat, perc_tropics, perc_south_mid_lat, perc_antarctic

def mean_sea_level_acquaterra(sea_level):
    n_pixels=float(len(sea_level))
    mean_sl=0.
    for level in sea_level:
        mean_sl+=level
    mean_sl=mean_sl/n_pixels
    
    return mean_sl
    
def mask_pixels_acquaterra(long_acquaterra, lat_acquaterra, long_global, lat_global):
    assert len(long_acquaterra)==len(lat_acquaterra)
    assert len(long_global)==len(lat_global)

    sort_coordinates(long_acquaterra, lat_acquaterra)
    sort_coordinates(long_global, lat_global)
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
    assert j==n_pixels_acquaterra
    return mask_pixels_acquaterra

def read_file_coordinates(file_name):
    os.chdir(dir_data)
    long=np.genfromtxt(file_name, comments='#', usecols=(0), dtype='f8')
    lat=np.genfromtxt(file_name, comments='#', usecols=(1), dtype='f8')
    
    return long, lat

def save_coord_distrib_as_txt_file(long_distrib, lat_distrib, file_name):
    assert len(long_distrib)==len(lat_distrib)
    os.chdir(dir_output)

    n_distrib=len(long_distrib)
    res=np.zeros(n_distrib, dtype=[("var1",float),("var2",float)])
    res["var1"]=long_distrib
    res["var2"]=lat_distrib
    f=open(nome_file+".dat","w")
    np.savetxt(f,res,delimiter="",fmt="%f\t %f\t", newline=os.linesep, header="longitude\t latitude\t\t")
    f.close()
    

    


def main():
    

    #Determination of acquaterra (AT) distribution
    file_CF_LGM="continent.026.0.dat"
    file_CF_present_day="continent.000.0.dat"

    long_CF_LGM, lat_CF_LGM= read_file_coordinates(file_CF_LGM)
    long_CF_present_day, lat_CF_present_day= read_file_coordinates(file_CF_present_day)
    
    long_acquaterra, lat_acquaterra=pixels_inundated(long_CF_LGM,
                                                     lat_CF_LGM,
                                                     long_CF_present_day,
                                                     lat_CF_present_day)

    #Save the output
    file_name="distribution_acquaeterra.dat"
    save_coord_distrib_as_txt_file(long_acquaterra, lat_acquaterra, file_name)
   

    #Determination history acquaterra

    n_pixels_history_AT=np.zeros(n_time_step)
    for j in range(n_time_step):
        file_name="continent."+labels_time_step[j]+".dat"
        long_CF_current, lat_CF_current= read_file_coordinates(file_name)

        long_AT_current, lat_AT_current=pixels_inundated(long_acquaterra,
                                                         lat_acquaterra,
                                                         long_AT_current,
                                                         lat_AT_current)
            
        
        nome_file="coordinates_acquaterra"+labels_time_step[j]
        save_coord_distrib_as_txt_file(long_AT_current, lat_AT_current, file_name)
        n_pixels_history_AT[j]=len(long_AT_current)

    history_acquaterra=n_pixels_history_AT/n_tot_pixel*100.
    history_acquaterra=np.flip(history_acquaterra)
    history_acquaterra=history_acquaterra*earth_area*0.01*10**(-3.)

    derivata_area=np.zeros(len(storia_acquaterra))
    for i in range(len(storia_acquaterra)):
        if i==0:
            derivata_area[i]=(storia_acquaterra[i+1]-storia_acquaterra[i])*2.
        elif i==len(storia_acquaterra)-1:
            derivata_area[i]=(storia_acquaterra[i]-storia_acquaterra[i-1])*2.
        else:
            derivata_area[i]=((storia_acquaterra[i]-storia_acquaterra[i-1])*2.+(storia_acquaterra[i+1]-storia_acquaterra[i])*2.)*0.5


    plt.figure(figsize=(10,6))
    time_step=np.arange(26,-0.5,-0.5)
    os.chdir(dir_plot)
    plt.xlim(26,0)
    plt.plot(time_step,storia_acquaterra, color="r", linestyle='-', lw=1, marker='o', markersize=3)
    plt.xlabel('year BP [kyr]', fontsize=15)
    plt.ylabel('Area acquaterra [km^2 * 10^3]', fontsize=15)
    #plt.yticks(np.arange(0,4,0.5))
    plt.xticks(np.arange(26,-1,-2))
    plt.savefig('graph_time_evolution_acquaterra.png', dpi=150)



    plt.figure(figsize=(10,6))
    time_step=np.arange(26,-0.5,-0.5)
    os.chdir(dir_plot)
    plt.xlim(26,0)
    plt.plot(time_step,derivata_area, color="b", linestyle='-', lw=1, marker='o', markersize=3)
    plt.xlabel('year BP [kyr]', fontsize=15)
    plt.ylabel('Derivata area acquaterra [km^2 * 10^3 \ 500 yr]', fontsize=12)
    #plt.yticks(np.arange(0,4,0.5))
    plt.xticks(np.arange(26,-1,-2))
    plt.axvspan(14.8,12.3, facecolor="#a2c4c9", alpha=0.3, edgecolor="black", linestyle="--", label="WMP-1a")
    plt.axvspan(11.5,8.8, facecolor="#a9c9a2", alpha=0.3, edgecolor="black", linestyle="--", label="WMP-1b")
    ##plt.annotate("WMP-1a", xy=(14.8,0.), fontsize=12)
    ##plt.annotate("WMP-1b", xy=(11.5,0.), fontsize=12)
    plt.legend(loc="lower right", fontsize=14)

    plt.savefig('derivata_area_acquaterra.png', dpi=150)

    return

if __name__=="__main_":
    main()
