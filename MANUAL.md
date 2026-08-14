# Introduction
The background theory of this project can be found in the introduction of `README.md` file available in the
project repository while a brief review is given throughout  this document where it is needed.

This manual text is organized into four chapters: Configuration, Input data, Method and Output data and plots.

In **Configuration**, we show the dependencies of our code as well as the easy way to run it.

In **Input data**, we describe how the format of the input files must be.

In the **Method** chapter, we illustrate the approach we used to solve the problem, describing the main function
we developed.

Finally in **Output data and plots**, we show the various results of the project; specifically, 
how the output data are formatted and how the plots are parametrized.

# Configuration
This project has been entirely written in `Python` language and it is proven to work in the `3.8`, `3.9`, `3.10`, `3.11`, 
`3.12` and `3.13` versions. Furthermore, the following python modules are used:
- numpy
- matplotlib.pyplot

After downloading the entire repository from [here](https://github.com/michaelmazon03/DistributionAcquaterra.git),
you can execute the code by running the following command in your terminal in the project directory:

```bash
python3 distribution_acquaterra.py
```

# Input data
As already pointed out in the `README.md` file, this project strongly exploits the output of **SELEN**, an open
source software which solves the *sea-level equation* (SLE). One of the most peculiar characteristic of SELEN is that it 
works on an icosahedron-based pixelization of Earth's surface; in other words, it  divide the Earth's surface into
 several pixels with about the same area and shape. This pixelization can be parametrized by a **resolution R** value. 
Given a certain value of R, the total number of pixels the Earth's surface is divided in is:

$$
n_{\text{pixel}}=\frac{40R(R-1)}{12}
$$

The area of each pixel is about:

$$
A_{\text{pixel}}=\frac{4\pi a^2}{n_{pixel}}
$$

where _a_ is the Earth's radius (the numerator $4\pi a^2$ is the total area of the Earth's surface) and $n_{\text{pixel}}$
is the total number of pixels.

The  input data our main code relies on are associated to the **Continent function** (CF) and the **Topography**. 
The CF is a mask function which is defined on the Earth's surface and at any given time; in other words, it is a 
function of the angular variable $\gamma=\gamma(\theta,\lambda)$ where $\theta$ is the latitude and $\lambda$ 
is the longitude. More specifically, the CF
is equal to 1 in the points on Earth's surface (or in  the pixels) where the land is exposed. While CF is equal
to zero in the points (or pixels) which are submerged below the ocean. Mathematically, at a given time $t", it can be defined as:

$$
CF(\gamma,t) = 
\begin{cases} 
      1 & \text{if } \hspace{0.5cm} \gamma \text{ is exposed land}\\
      0 & \text{if } \hspace{0.5cm} \gamma \text{ is covered by water}
\end{cases}  
$$

The topography T is also a function of the position on Earth's surface and the time: $T=T(\gamma,t)$; and is defined
as the opposite of the so called **sea-level** (SL) which is the height of the sea-surface (or the geoid) with 
respect to the solid earth's surface. As the geoid is a constant gravitational potential surface, both the the topography
and sea-level can be determined in the dry land and in the ocean.

SELEN determines the CF and the topography, among other quantities, solving the **sea-level equation** in several
epochs between the last glacial maximum (LGM), occurring about 21 and 26 kyr BP (kilo-years Before Present),
and the present-day (0 kyr BP); with a certain time-step, typically 1 or 0.5 kyr.


## Data input format
A test data input is given in the project repository at the `data` directory; however, the user can use its own data
if it is properly formatted as we will describe hereafter.\
The files in `data` have been directly taken from the output of SELEN, therefore the name and the format of the 
files are the ones defined for the output of SELEN. 

The files are associated with the two quantities we are interested in, the continent function and the topography; and they are
named as:

- `continent.0xx.x.dat`
- `topo.0xx.x.dat`

where the prefix `0xx.x` represents the time in terms of kyrs BP. For example, 
`continent.000.0.dat` and `continent.011.5.dat` describe the solution for the continent function at the present-day
(0 kyr BP) and at 11.5 kyr BP, respectively.

### Continent function data
The `continent.0xx.x.dat` files consist of two columns which represent the **longitudes** and **latitudes**; where the rows
are the coordinates of the pixels in which, at that time (`0xx.x`), the CF is equal to 1. The longitudes are conventionally
defined between 0° and 360°, while the latitudes are defined between -90° and 90°. It is worth noting that the 
pixels listed in the continent files are a subset of the pixels that are obtained by the icosahedron-based pixelization
with a certain resolution;  therefore the number of rows must be less than or equal to the number of the pixels
in the set defined by the pixelization, $n_\text{pixels}$.

### Topography data
The `topo.0xx.x.dat` files consist  of three columns: **longitudes**, **latitudes** and **topography**; each file describes the topography
field on the Earth's surface at the epoch 0xx.x kyr BP. Therefore, the number of rows coincides with the total number
of pixels with which the Earth's surface has been divided by the pixellization and each row contains the value of topography
for that pixel. The longitudes are conventionally defined between 0° and 360°, the latitudes are defined between -90° and 90°
and the topography is expressed in meters [m].

If the user want to use its own data, beside the fact the input file must be formatted as described above,
these data must be previously interpolated in a proper icosahedron-based pixelization system or, in general, in
a set of pixels with the same area, since many computetion made inside our code strongly rely on this property.

The test data input made avaible in the repository project has been obtain by a SELEN simulation with a resolution 
of R=44.

# Method
After proceeding to the description of the structure and the method used in the project, it is worth remembering the
aim of this work, that is, the determination of acquaterra spatial distribution and its time evolution; throughout the project
we will also evaluate some statistics of acquaterra. A more detailed description of the background theory can be found
in the introduction of `README.md`, here we remember that the acquaterra 
is the global region of Earth's surface that has been inundated from the last glacial maximum (the period of maximum 
extension of the ice-sheets occurring about 26,000 yr BP) and the present day due to the rising sea-level.

The main code `distribution_acquaterra.py` has been organized with a `main` function that calls several other
functions properly designed to read and elaborate the data input and to save and plot the results.

In the project we follow these steps:

1. We determine the **Acquaterra distribution**;
2. then, we compute some **statistics** of acquaterra such as: the mean sea-level on acquaterra, the zonal distribution and
a regional distribution of acquaterra;
3. finally, we calculate the **time evolution** of acquaterra.

The order of the steps shown above is random, but they are strongly linked to each other since the acquaterra distribution
(`step 1`) is required to evaluate both the statistics and the history of acquaterra 
(`step 2` and `step 3`, respectively).

## Step 1: distribution acquaterra
As already said before, we define the acquaterra (AT) distribution as the global region that has been inundated from the LGM 
(which, in our test data input, is fixed at 26 kyr BP) to the present day (0 kyr BP). Therefore, we proceed by reading
 the data input files of the continent function (CF) at LGM `continent.026.0.dat` and at present day 
`continent.000.0.dat` using the function `read_file_coordinates`; then, we compare those CF distributions; specifically,
 we look for those pixels that are present in `continent.026.0.dat` and that have disappeared in `continent.000.0.dat`.
 In other words, we look for those pixels that have been "inundated". This distribution is the desired acquaterra distribution and
 we perform this computation with the function `pixels_inundated`.\
These operations are performed at the beginning of the `main` function:

```python
def main():
    
	#Determination of acquaterra (AT) distribution
    logging.info("Computing distribution acquaterra...")
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
```

The `read_file_coordinates` function takes the name of the input txt file  and returns the coordinates
of the distribution as separated numpy arrays (`long` and `lat`) using the numpy function `np.genfromtxt`:
 
```python
def read_file_coordinates(file_name):
    #os.chdir(dir_data)
    long=np.genfromtxt(dir_data / file_name, comments='#', usecols=(0), dtype='f8')
    lat=np.genfromtxt(dir_data / file_name, comments='#', usecols=(1), dtype='f8')
    return long, lat
```

The `sort_coordinates_lexsort` function sorts the array coordinates first by ascending latitudes, then by
ascending longitudes. This operation is required because the `pixels_inundated` function has been initially designed
with coordinate arrays properly sorted as input variables.

Here is what `pixels_inundated` looks like:

```python
def pixels_inundated(start_long, start_lat, end_long, end_lat):

	end_long_test=end_long
	end_lat_test=end_lat
	n_pixels_start=len(start_long)
	mask_pixels_inundated=[]

	for j in range(n_pixels_start):
		mask_lat_is_in=np.isin(  end_lat_test, start_lat[j])
		mask_long_is_in=np.isin(end_long_test,start_long[j])
		mask_coord_is_in=np.logical_and(mask_lat_is_in,mask_long_is_in)
		pixel_has_been_inundated=True
		if True in np.array(mask_coord_is_in):
			pixel_has_been_inundated=False
			index_pixel_in_end_coord=np.where(np.array(mask_coord_is_in)==True)
			index=index_pixel_in_end_coord[0]
			end_long_test=end_long_test[index[0]:]
			end_lat_test=end_lat_test[index[0]:]
            
		mask_pixels_inundated.append(pixel_has_been_inundated)

	lat_pixels_inundated=start_lat[mask_pixels_inundated]
	long_pixels_inundated=start_long[mask_pixels_inundated] 
    
    return long_pixels_inundated, lat_pixels_inundated
```
 
This function takes two spatial distributions as input: the initial distribution identified by `start_long` and `start_lat`
and the final distribution described by `end_long` and `end_lat`; and searchs for the difference between those distributions
exploiting the numpy built-in operation with the boolean mask as the operation of slicing with mask array and the function 
`np.isin`.\
Finally, the function returns  the results in terms of coordinate numpy arrays: `long_pixels_inundated`, 
`lat_pixels_inundated`.

## Step 2: Statistics
After computing the acquaterra distribution, we are ready to calculate some statistics and quantities associated
with acquaterra itself, such as:

- total **global area** of acquaterra;
- the present day **mean sea level** in the acquaterra region;
- a certain subregion of acquaterra and its area and mean sea level;
- the zonal distribution of acquaterra.

### Area and mean sea level of acquaterra
Perhaps the most convenient features of the icosahedron-based pixelization on which **SELEN** and our code
rely on is that the pixels through which we divide the Earth's surface have about the same area. At the beginning
of the code we list some important parameters associated with the geometry of Earth and its pixelization:

```python
#Earth's parameters
earth_radius=6371.
R=100
n_total_pixels=40*R*(R-1)+12
area_pixels=(4*np.pi*earth_radius**2)/float(n_total_pixels)
earth_area=4.*np.pi*earth_radius**2.
```

Therefore the total area of acquaterra can be easily evaluated as the total number of pixels of AT distribution
times the area of each pixel (`area_pixels`).

```python
def main():
	...
	
	#area acquaterra
    n_pixels_AT=len(long_acquaterra)
    area_AT=n_pixels_AT*area_pixels
	
	...
```

To calculate the present day mean sea level on AT we use the topography input data the format of which has been
described in the **input data** section. Thus, we read the `topo.000.0.dat` with a proper function. Furthermore, we 
remember that the sea level (SL) is the opposite of the topography (T): $SL(\gamma,t)=-T(\gamma,t)$.

```python
def main():
	...

	#MEAN SEA-LEVEL on acquaterra (AT)
	
    #reading file topography
    file_name='topo.000.0.dat'
    long_global, lat_global, topography= read_file_field_on_earth_suf(file_name)
    sea_level=topography*(-1.)
	
    logging.info("Computing mean sea level on acquaterra")
    sort_coordinates_lexsort(long_acquaterra, lat_acquaterra)
    mask_sea_level_AT=mask_pixels_acquaterra(long_acquaterra, lat_acquaterra, long_global, lat_global)
    sea_level_AT=sea_level[mask_sea_level_AT]
    mean_SL_AT=np.mean(sea_level_AT)

	...
```

we remember that the `topo.0xx.x.dat` files contain the topography field on the entire Earth's surface; in other words,
they give, for each pixel, the value of topography, so they have all the pixels of the pixelization of Earth's surface.
Therefore, after sorting the coordinate arrays of both the acquaterra (`long_acquaterra` and `lat_acquaterra`)
and the global Earth (`long_global` and `lat_global`), we exploit the `mask_pixels_acquaterra` function which takes these 
arrays as input and returns a boolean mask `mask_sea_level_AT` which describes the pixels of acquaterra on the
global coordinate arrays. Finally, we obtain the array of sea level on AT by applying the operation of slicing with
the boolean mask above and since all the pixels have the same area, we can evaluate the mean sea level on AT 
`mean_SL_AT` by a simple mean operation (we used `np.mean`).

### Regional Acquaterra
Here we compute the same quantities as the previous section (so, the area and the mean sea-level) but we consider
a subregion of AT. To do so we exploit the function `regional_acquaterra`:

```python
def regional_acquaterra(long_min, long_max, lat_min, lat_max, long_acquaterra, lat_acquaterra):
...

```

This function takes a rectangular region on Earth's surface in terms of coordinates limits (`long_min`, `long_max`, 
`lat_min`, `lat_max`) and the coordinate arrays of AT distribution and returns the coordinate arrays of AT of the
pixels which are inside the subregion taken into account. It is worth remembering that in the convention of this project the longitudes
are defined between 0° and 360°; thus, `long_min` can be greater than `long_max` if the subregion contains the 0°
meridian. The proper functioning of the function in this case has been tested in `test_distribution_acquaterra.py`.

### Zonal Acquaterra
In this part we evaluate the distribution of AT in the different zonal regions (regions delimited between two latitudes).
This computation is performed by the function `percentage_zonal_distrib_AT` inside of which we conventionally defined the 
following regions with the latitude limits:

- Arctic (from 90° to 66°)
- Northern mid-latitudes (from 66° to 23°)
- Tropics (from 23° to -23°)
- Southern mid-latitudes (from -23° to -66°)
- Antarctic (from -66° to -90°)

```python
def percentage_zonal_distrib_AT(long_acquaterra, lat_acquaterra):
...

```

This function takes simply the AT coordinate arrays and gives the percentage of the AT area on each zonal region 
defined above. It is worth  noting that we don't consider the pixels that sit exactly in the latitudes boundaries (that
are 90°, 66°, 23°, -23°, -66° and -90°). Since the number of the pixels is very high we evaluated that we do 
not make a big mistake by doing so. This property of the function has been tested in `test_distribution_acquaterra.py`.

## Step 3: Acquaterra History
In this last part, we calculate the time evolution of AT exploiting the  files `continent.0xx.x.dat` associated
with intermediate epochs. We already described the format of these files in the `data input` section in this document.


```python
main():
...

	#Determination history acquaterra
    logging.info("Computing time history of acquaterra")
    n_pixels_history_AT=np.zeros(n_time_step)
    for j in range(n_time_step):
        logging.debug("Computing distribution acquaterra at epoch "+labels_time_step[j]+" kyr BP")
        file_name="continent."+labels_time_step[j]+".dat"

        long_CF_current, lat_CF_current= read_file_coordinates(file_name)
        sort_coordinates_lexsort(long_CF_current,lat_CF_current)
        long_AT_current, lat_AT_current=pixels_not_inundated(long_acquaterra,
                                                         lat_acquaterra,
                                                         long_CF_current,
                                                         lat_CF_current)
            
        file_name="coordinates_acquaterra"+labels_time_step[j]+".txt"
        save_coord_distrib_as_txt_file(long_AT_current, lat_AT_current, file_name)
        n_pixels_history_AT[j]=len(long_AT_current)

    history_acquaterra=n_pixels_history_AT/n_total_pixels*100.
    history_acquaterra=np.flip(history_acquaterra)
    history_acquaterra=history_acquaterra*area_pixels*0.01*10**(-3.)

    time_step=0.5
    time_derevative_AT=time_derevative_function(history_acquaterra, time_step)

```
Here, at each iteration  of the loop we obtain the continent function (the coordinate arrays) for a certain epoch (`0xx.x` kyr BP)
 by reading the file `continent.0xx.x.dat`; then we compare the AT distribution with the CF distribution of 
 that intermediate epoch. More specifically, we look for those pixels of the AT which are still present in the intermediate
 epoch; in other words, they are the pixels that have not been inundated yet at that time. We perform this operation
 with the function `pixels_not_inundated`. Furthermore, for each time
 we count the number of these pixels and we store them in the numpy array called `n_pixels_history_AT`.
 Then, we convert this into AT area exploiting the fact that each pixel has the same area as we have 
 done before.
 
Moreover, we compute the time derivative of the area of AT using the function `time_derevative_function`. This takes
the array of the time evolution of AT area and the time step (expressed in kyr) as input and performs a difference
finite derivative.
 
 
# Output data and plots
In this last section we the results of our project are shown. We will describe the meaning and the format of the content
of the output. 

When the code is executed,  two directories, `output` and `plot`, are created.

## Output directory
The `output` directory contains itself the following other subfolders:

- distribution_acquaterra
- history_acquaterra
- statistics_acquaterra

### distribution_acquaterra folder
Here you can find the `distribution_acquaterra.dat` txt file which is the final result of the step 1 in the `main`
function. We have described this part of the function `main` in the `method` section of this document. The definition
of the **acquaterra** distribution has been introduced in detail in `README.md` file; a brief review can be found
in the subsection `Step 1` in this document.

The `distribution_acquaterra.dat` contains two columns: `longitudes` and `latitudes`. Conventionally, `longitudes`
are expressed between 0° and 360°, while `latitudes` are defined between -90° and 90°.

Also, in the same directory there is `distribution_AT_mediterranean_sea.dat` file. This is the result of the
`regional_acquaterra` function that is performed in `Step 2` among the computation of the statistics of AT. Its content
and the format are the same as `distribution_acquaterra.dat`. As default, in  `regional_acquaterra` we use a rectangular
region centered to the Mediterranean Sea but the user can use every desired region modifying the coordinates limits
as variables input for the `regional_acquaterra` function.

### History_acquaterra folder
In this directory, the txt files `acquaterra.0xx.x.dat` are present. These files are the results of the 
`Step 3` in the `main` function described in the `method`. Here we used the same convention for the prefix 
`0xx.x` as for the `data` input files; that is, `0xx.x` represents the epoch in kilo-years before present (kyr BP).
Thus, for example `acquaterra.026.0.dat`, `acquaterra.010.5.dat` and `acquaterra.00.0.dat` are, respectively,
the distribution at the last glacial maximum (26 kyr BP), at 10.5 kyr BP and at present day (kyr BP). Specifically, each
file contains the list of pixels of acquaterra which, at that epoch, have not been "inundated" yet; or in other words,
it contains the pixels of AT where the continent function is equal to 1. It is worth remembering that the acquaterra
distribution  has been defined and computed as the comparison between the CF at the last glacial maximum (26 kyr BP) 
and the present day and does not take into account the intermediate epochs.

The files `acquaterra.0xx.x.dat` have the same format of  `distribution_acquaterra.dat` file 
described above; that is, it contains two columns: `longitudes` and `latitudes`. Conventionally, `longitudes`
are expressed between 0° and 360°, while `latitudes` are defined between -90° and 90°.


### Statistics_acquaterra folder
Here you find `statistics_acquaterra.dat` that contains the results of the `Step 2` of the `main` function
regarding the statistics of AT. Specifically, there is the **total area** and the **mean sea-level** of the global
distribution of AT, the total area and mean sea-level of a limited rectangular region on Earth's surface, by default
the Mediterranean sea is considered, and finally the zonal distribution of AT.

## Plot
In this directory, two plots are present. They are named `graph_evolution_acquaterra_area.png` and 
`graph_AT_area_time_derivative.png` and feature respectively, the time evolution of the area of the dry land of AT
 and its time derivative:
 
- `graph_evolution_acquaterra_area.png` has  the time (in kyr BP) on the x axis and the area in unit of
[$\text{km}^2 \times 10^3$] on the y axis
- `graph_AT_area_time_derivative.png` feature  the time (in kyr BP) on the x axis and the time derivative of the area 
in units of [$\text{km}^2 \times 10^3/ 500 \text{yr}$] on y axis.

