# Introduction
This project has been entirely written in `Python` language and it is proven to work in the `3.8`, `3.9`, `3.10`, `3.11`, 
`3.12` and `3.13` versions. Furthermore, the following python modules are used:
- numpy
- matplotlib.pyplot
After downloading the entire repository from [here](https://github.com/michaelmazon03/DistributionAcquaterra.git)
you can execute the code by running the following command in your terminal in the project directory:

```bash
python3 distribution_acquaterra.py
```

This document is organized into three chapters: input data, method and output data and plots.

In **Input data**, we describe how the format of the input files must be.

In the **method chapter**, we illustrate the approach we used to solve the problem, describing the main function
we developed.

Finally in **Output data and lots**, we show the several results of the project; specifically, 
how the output data are formatted and how the plots are parametrized.

# Input data
As already pointed out in the `README.md` file, this project strongly exploits the output of **SELEN**, an open
source software which solves the *sea-level equation* (SLE). One of the most peculiar characteristic of SELEN is that it 
works on an icosahedron-based pixelization of Earth's surface; in other words, it is divided in several pixels
with about the same area and shape. This pixelization can be parametrized by a **resolution R** value. Given a
certain value of R, the total number of pixels the Earth's surface is divided in is:

$$
n_{\text{pixel}}=\frac{40R(R-1)}{12}
$$

The area of each pixel is about:

$$
A_{\text{pixel}}=\frac{4\pi a^2}{n_{pixel}}
$$

where _a_ is the Earth's radius (the numerator $4\pi a^2$ is the total area of the Earth's surface) and $n_{\text{pixel}}$
is the total number of pixels.

The  input data our main code relies on is associated to the **Continent function**(CF) and the **Topography**. 
The CF is a mask function which is defined on the Earth's surface and at any given time; in other words, it is a 
function of the angular variable $\gamma=\gamma(\theta,\lambda)$ where $\theta$ is the latitude and $\lambda$ 
is the longitude. More specifically, the CF
is equal to 1 in the points on Earth's surface (or in  the pixels) where the land is exposed. While CF is equal
to zero in the points (or pixels) which are submerged below the ocean. Mathematically, it can be defined as:

$$
CF(\gamma,t) = 
\begin{cases} 
      1 & \text{if } \hspace{0.5cm} \gamma \text{ is exposed land}\\
      0 & \text{if } \hspace{0.5cm} \gamma \text{ is covered by water}
\end{cases}  
$$

The topography T is also a function of the position on Earth's surface and the time $T=T(\gamma,t)$ and is defined
as the opposite of the so called **sea-level** (SL) which is the height of the sea-surface (or the geoid) with 
respect to the solid earth's surface. As the geoid is a constant gravitational potential surface, both the the topography
and sea-level can be determined in the dry land and in the ocean.

SELEN determines the CF and the topography, among other quantities, solving the **sea-level equation** in several
epochs between the last glacial maximum (LGM), occurring about 21 and 26 kyr BP (kilo-years Before Present),
and the present-day (0 kyr BP); with a certain time-step, typically 1 or 0.5 kyr.


## Data input format
A test data input is given in the project repository at the `data` directory; however, the user can use their own data
if it is properly formatted as we will describe hereafter.\
The files in `data` have been directly taken from the output of SELEN, therefore the name and the format of the 
files are the ones defined for the output of SELEN. 

The files are associated to the two quantities we are interested in, the continent function and the topography; and they are
named as:

- `continent.0xx.x.dat`
- `topo.0xx.x.dat`

where the prefix `0xx.x` represents the time in terms of kyrs BP. For example, 
`continent.000.0.dat` and `continent.011.5.dat` describe the solution for the continent function at the present-day
(0 kyr BP) and at 11.5 kyr BP, respectively.

### continent function data
The `continent.0xx.x.dat` files consist in two columns which represent the **longitudes** and **latitudes**; where the rows
are the coordinates of the pixels in which, at that time (`0xx.x`), the CF is equal to 1. The longitudes are conventionally
defined between 0° and 360°, while the latitudes are defined between -90° and 90°. It is worth to note that the 
pixels listed in the continent files are among the pixels that are obtained by the icosahedron-based pixelization
with a certain resolution; and therefore the number of rows must be less than or equal to the number of the pixels
in the set defined by the pixelization, $n_\text{pixels}$, and it is more likely to be less.

### topography data
The `topo.0xx.x.dat` files consist  in three columns: **longitudes**, **latitudes** and **topography**; it describes the topography
field on the Earth's surface at the epoch 0xx.x kyr BP. Therefore, the number of rows coincides with the total number
of pixels with which the Earth's surface have been divided by the pixellization and each row is the value of topography
for that pixel. The longitudes are conventionally defined between 0° and 360°, the latitudes are defined between -90° and 90°
and the topography is expressed in meters [m].

# Method
After proceeding to the description of the structure and the method used in the project, it is worth remembering the
aim of this work, that is the determination of acquaterra spatial distribution and its time evolution; throughout the project
we will also evaluate some statistics of acquaterra. A more detailed description of the background theory can be found
in the introduction of `README.md`, here we remember that the acquaterra 
is the global region of Earth's surface that has been inundated from the last glacial maximum (the period of maximum 
extension of the ice-sheets occurring about 26,000 yr BP) and the present day due to the rising sea-level.

The main code `distribution_acquaterra.py` has been organized with a `main` function that calls several other
functions properly designed to read and elaborate the data input and to save and plot the results.

In the project we follow these steps:

1. We determine the **Acquaterra distribution**;
2. then we compute some **statistics** of acquaterra such as the mean sea-level on acquaterra, the zonal distribution and
a regional distribution of acquaterra;
3. finally, we calculate the **time evoluton** of acquaterra.

The order of the steps above is random but they are strongly linked to each other, since the acquaterra distribution
(`step 1`) is required to evaluate both the statistics and the history of acquaterra 
(`step 2` and `step 3`, respectively).

## Step 1: distribution acquaterra
As already said before, we define the AT distribution as the global region that has been inundated from the LGM 
(which, in our test data input, is fixed at 26 kyr BP) to the present day (0 kyr BP). Therefore, we proceed reading
 the data input files of the continent function (CF) at LGM `continent.026.0.dat` and at present day 
`continent.000.0.dat` using the function `read_file_coordinates`; then, we compare those CF distributions; specifically,
 we look for those pixels that are present in `continent.026.0.dat` and that have been disappeared in `continent.000.0.dat`.
 In other words, we look for those pixels that have been "inundated". This distribution is the desired acquaterra distribution and
 we perform this computation with the function `pixels_inundated`:
 
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
 
this function takes two spatial distribution as input: the initial distribution identified by `start_long` and `start_lat`
and the final distribution described by `end_long` and `end_lat`; and search for the difference between those distributions
exploiting the numpy built-in operation with the boolean mask as the operation of slicing with mask array and the function 
`np.isin`.







# Output data and plots