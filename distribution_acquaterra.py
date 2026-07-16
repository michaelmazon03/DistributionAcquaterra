#importo librerie
import os
import numpy as np
import matplotlib.pyplot as plt

#definizione directory e file
dir_home=os.getcwd()
dir_output=dir_home+"\\output"

if not(os.path.isdir(dir_output)):
    os.mkdir("output")

labels_time_step=["000.5","001.5","002.5","003.5","004.5","005.5","006.5","007.5","008.5","009.5",
                  "010.5","011.5","012.5","013.5","014.5","015.5","016.5","017.5","018.5","019.5",
                  "020.5","021.5","022.5","023.5","024.5","025.5"]
#suf_time_step1=["001.0","002.0","003.0","004.0","005.0","006.0","007.0","008.0","009.0","010.0","011.0","012.0","013.0","014.0","015.0","016.0","017.0","018.0","019.0","020.0","021.0","022.0","023.0","024.0","025.0"]

n_time_step=len(labels_time_step)
matrice_tot_OF=[]
lista_n_pixel_OF=[]

def sort_coordinates(long,lat):
    n_coord=len(long)
    for i in range(n_coord):
        long_test=long[i]
        lat_test=lat[i]
        n_cycles=n_coord-i
        index_min=i
        for j in range(n_cycles):
            if lat_test>=lat[i+j] and long_test>long[i+j]:
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
        for i in range(n_pixels_long):
            if start_long[j]==end_long[i] and start_lat[j]==end_lat[i]:
                pixel_has_been_inundated=False
                np.delete(end_long_test, range(0,i))
                np.delete(end_lat_test, range(0,i))
                break
        
        mask_pizels_inundated.append(pixel_has_been_inundated)
    lat_pixels_inundated=start_lat[mask_pixels_inundated]
    long_pixels_inundated=start_long[mask_pixels_inundated]
    
    return long_pixels_inundated, lat_pixels_inundated
    
def determine_distrib_acquaterra(long_lgm, lat_lgm, long_present_day, lat_present_day):
    long_lgm, lat_lgm=sort_coordinates([logn_lgm,lat_lgm])
    long_present_day, lat_present_day=sort_coordinates([logn_present_day,lat_present_day])
    distrib_acquaterra=pixels_inundated(long_lgm, lat_lgm, long_present_day_lat(present_day))
    
    
    return distrib_acquaterra

def determine_history_acquaterra(labels_time_step):

    return history_acquaterra


def main():
    determine_distrib_acquaterra()
    determine_history_acquaterra()

    
    

 
    dir_file_acquaterra=dir_output+"\\coordinate_acquaterra.dat"
    file_primo_step="continent.026.0.dat"
    file_ultimo_step="continent.000.0.dat"

    long_primo_step=np.genfromtxt(file_primo_step, comments='#', usecols=(0), dtype='f8')
    lat_primo_step=np.genfromtxt(file_primo_step, comments='#', usecols=(1), dtype='f8')
    long_ultimo_step=np.genfromtxt(file_ultimo_step, comments='#', usecols=(0), dtype='f8')
    lat_ultimo_step=np.genfromtxt(file_ultimo_step, comments='#', usecols=(1), dtype='f8')
    n_primo=len(long_primo_step)
    n_ultimo=len(long_ultimo_step)

    coord_primo=[]
    coord_ultimo=[]
    mask_coord_acquaterra=[]
    coord_acquaterra=[]
    print("sto generando lista coordinate file "+file_primo_step)
    for i in range(n_primo):
        coppia=np.zeros(2)
        coppia[0]=long_primo_step[i-1]
        coppia[1]=lat_primo_step[i-1]
        coord_primo.append(coppia)

    print("sto generando lista coordinate file "+file_ultimo_step)
    for i in range(n_ultimo):
        coppia=[]
        coppia.append(long_ultimo_step[i-1])
        coppia.append(lat_ultimo_step[i-1])
        coord_ultimo.append(coppia)

    copia_coord_ultimo=coord_ultimo
    n_copia_ultimo=len(copia_coord_ultimo)
    n_veri=0
    n=0
    for coord in coord_primo:
        n=n+1
        if n==100:
            print("ho anallizzato 100 pixel")
        elif n==500:
            print("ho anallizzato 500 pixel")
    
        for i in range(n_copia_ultimo):
            coord_confronto=copia_coord_ultimo[i]
            if coord[0]==coord_confronto[0] and coord[1]==coord_confronto[1]:
                cond=False
                copia_coord_ultimo.remove(coord_confronto)
                n_copia_ultimo=n_copia_ultimo-1
                break
        if cond==True:
            n_veri=n_veri+1
        mask_coord_acquaterra.append(cond)
        if n_veri==10:
            print("ho trovato 10 pixel")
        elif n_veri==50:
            print("ho trovato 50 pixel")

    print("ho finito la ricerca dei pixel dell'acquaterra")
    print("pixel tempo presente che hanno C=1 ma che avevano C=0 in t=26 kyr: "+str(n_copia_ultimo))

    n=len(coord_primo)
    lat_acquaterra=np.zeros(n)
    long_acquaterra=np.zeros(n)
    for i in range(n):
        coord=coord_primo[i]
        lat_acquaterra[i]=coord[1]
        long_acquaterra[i]=coord[0]

    lat_acquaterra=lat_acquaterra[mask_coord_acquaterra]
    long_acquaterra=long_acquaterra[mask_coord_acquaterra]



    os.chdir(dir_output)

    n_acquaterra=len(long_acquaterra)
    res=np.zeros(n_acquaterra, dtype=[("var1",float),("var2",float)])
    res["var1"]=long_acquaterra
    res["var2"]=lat_acquaterra
    nome_file="coordinate_acquaterra"
    f=open(nome_file+".dat","w")
    np.savetxt(f,res,delimiter="",fmt="%f\t %f\t", newline=os.linesep, header="longitude\t latitude\t\t")
    f.close()


    os.chdir(dir_home)
    file_primo_step="continent.026.0.dat"
    long_primo_step=np.genfromtxt(file_primo_step, comments='#', usecols=(0), dtype='f8')
    lat_primo_step=np.genfromtxt(file_primo_step, comments='#', usecols=(1), dtype='f8')
    n_primo=len(long_primo_step)
    coord_primo=[]
    mask_coord_acquaterra=[]
    coord_acquaterra=[]

    print("sto generando lista coordinate file "+file_primo_step)
    for i in range(n_primo):
        coppia=np.zeros(2)
        coppia[0]=long_primo_step[i-1]
        coppia[1]=lat_primo_step[i-1]
        coord_primo.append(coppia)
    for i in range(n_acquaterra):
        coppia=np.zeros(2)
        coppia[0]=long_acquaterra[i-1]
        coppia[1]=lat_acquaterra[i-1]
        coord_acquaterra.append(coppia)

    n_pixels_storia_acquaterra=np.zeros(n_time_step+1)
    n_pixels_storia_acquaterra[0]=n_acquaterra
    for j in range(n_time_step):
    ##    coord=coord_primo[j]
        os.chdir(dir_home)
        file_name="continent."+suf_time_step[j]+".dat"
        longitudine=np.genfromtxt(file_name, comments='#', usecols=(0), dtype='f8')
        latitudine=np.genfromtxt(file_name, comments='#', usecols=(1), dtype='f8')
        n=len(longitudine)
        
        lista_n_pixel_OF.append(n)
        coordinate_corrente=[]
        print("sto leggendo il time step "+suf_time_step[j])
        latitudine_copia=latitudine
        longitudine_copia=longitudine
        for i in range(n):
            coppia=[]
            coppia.append(longitudine[i-1])
            coppia.append(latitudine[i-1])
            coordinate_corrente.append(coppia)

        
        n_coord_corrente=len(coordinate_corrente)
        coord_corrente_copia=coordinate_corrente
        n_veri=0
        n=0
        mask_confronto=[]
        for coord in coord_primo:
            n_coord_copia=len(coord_corrente_copia)
            n=n+1
            if n==10:
                print("ho anallizzato 10 pixel")
            elif n==50:
                print("ho anallizzato 50 pixel")
            elif n==100:
                print("ho anallizzato 100 pixel")
            elif n==500:
                print("ho anallizzato 500 pixel")
            elif n==1000:
                print("ho anallizzato 1000 pixel")
            elif n==100000:
                print("ho anallizzato 100000 pixel")
            elif n==150000:
                print("ho anallizzato 150000 pixel")
            elif n==200000:
                print("ho anallizzato 200000 pixel")
            cond=True
            for i in range(n_coord_copia):
                coord_confronto=coord_corrente_copia[i]
                if coord[0]==coord_confronto[0] and coord[1]==coord_confronto[1]:
                    cond=False
                    coord_corrente_copia.remove(coord_confronto)
                    break
            if cond==True:
                n_veri=n_veri+1
            mask_confronto.append(cond)
        print("ho finito confronto con file "+file_name)

        n=len(coord_primo)
        lat_acquaterra_corrente=np.zeros(n)
        long_acquaterra_corrente=np.zeros(n)
        for i in range(n):
            coord=coord_primo[i]
            lat_acquaterra_corrente[i]=coord[1]
            long_acquaterra_corrente[i]=coord[0]

        lat_acquaterra_corrente=lat_acquaterra_corrente[mask_confronto]
        long_acquaterra_corrente=long_acquaterra_corrente[mask_confronto]
        coord_AT_corrente=[]
        print("diffrenza fra i due file è: "+str(len(lat_acquaterra_corrente)))
        for i in range(len(lat_acquaterra_corrente)):
            coppia=[]
            coppia.append(long_acquaterra_corrente[i-1])
            coppia.append(lat_acquaterra_corrente[i-1])
            coord_AT_corrente.append(coppia)
        coordinate_confronto_copia=coord_AT_corrente
        print("sto facendo il confronto fra acquaterra_primo step con quello corrente")
        n=0
        mask_confronto_acquaterra=[]
        
        for coord in coord_acquaterra:
            n_coord_copia=len(coordinate_confronto_copia)
            n=n+1
            if n==1000:
                print("ho anallizzato 1000 pixel")
            elif n==5000:
                print("ho anallizzato 5000 pixel")
            elif n==10000:
                print("ho anallizzato 10000 pixel")
            elif n==15000:
                print("ho anallizzato 15000 pixel")
            cond=True
            for i in range(n_coord_copia):
                coord_confronto=coordinate_confronto_copia[i]
                if coord[0]==coord_confronto[0] and coord[1]==coord_confronto[1]:
                    cond=False
                    coordinate_confronto_copia.remove(coord_confronto)
                    print("ho trovat un vero")
                    break

            mask_confronto_acquaterra.append(cond)
            
        long_AT_corrente=long_acquaterra
        lat_AT_corrente=lat_acquaterra
        long_AT_corrente=long_AT_corrente[mask_confronto_acquaterra]
        lat_AT_corrente=lat_AT_corrente[mask_confronto_acquaterra]
        n_pixel_corrente=len(long_AT_corrente)
        print("il risultato per la storia del acquaterra è: "+str(n_pixel_corrente))
        print("ho finito confronto con file "+file_name)


        
        os.chdir(dir_output)
        n_pixels_storia_acquaterra[j+1]=n_pixel_corrente
        res=np.zeros(n_pixel_corrente, dtype=[("var1",float),("var2",float)])
        res["var1"]=long_AT_corrente
        res["var2"]=lat_AT_corrente
        nome_file="coordinate_acquaterra"+suf_time_step[j]
        f=open(nome_file+".dat","w")
        np.savetxt(f,res,delimiter="",fmt="%f\t %f\t", newline=os.linesep, header="longitude\t latitude\t\t")
        f.close()



    plt.figure(figsize=(14,10))
    time_step=np.arange(0.,26.,-0.5)
    plt.plot(time_step,n_pixels_storia_acquaterra, color="g", linestyle='-', marker='o', marker_size=10)
    plt.xlabel('year BP [kyr]')
    plt.ylabel('relative area acquaterra')
    plt.savefig('graph_time_evolution_acquaterra.png', dpi=150)

if __name__=="__main_":
    main()
