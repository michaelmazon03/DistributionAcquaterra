# DistributionAcquaterra

## Introduction ##



In the last 120,000 years,  Earth has been subjected to a complete glacial cycle. This consists of the following
phases: a slow accumulation of ice in the ice sheets (for about 100,000 years) which culinates in the period of maximum 
volume extension of the ice sheets called Last Glacial Maximum (LGM) which occours at about 26000 years BP (before
present). The LGM, in turns, is followed by a rapid 
melting of ice that finally leads to the interglacial condition, which is the present day condition starting 
about 6,000 years BP, where the ice-sheets result to be stable. Since a large amount of water was stored in 
the ice sheets, the LGM sea-level was significantly lower (about 130 m) than the present-day sea-level. Therefore,
there are large regions on Earth which were exposed at the LGM and that have been progressivelly inundated by the ocean
due to  the rising sea-level. These regions were named **Acquaterra** by Dobson; specifically, the acquaterra 
is defined as the regions on Earth that have been cyclically inundated and exposed due to the periodic accumulation
and retreat of ice-sheets, in the period starting from the time the modern human first appeared on the Earth.
Acquaterra is a strongly interdisciplinary topic that includes geography, archaeology, oceanography and geophysics.

In this project we numerically calculate the distribution of acquaterra exploiting the outputs of SELEN, an open 
source software which solves the _sea-level equation_ in its complete version; that is, it takes into account
the gravitational effects, the viscoelastic deformation of the Earth's interior, the migration of the coast lines and the effects
associated with the variation of the rotational axis of Earth. To do so, SELEN applies an icosahedron-based pixellization
which divides the Earth's surface into many pixels with about the same area; moreover, for each pixel, it determines
the sea-level, or analogously its inverse, that is the topography, in several epochs between the LGM and the
present day using a time-step of typically 500 years.

Among the many outputs given by SELEN we are interested in the solution of the **Continental Function** (CF).
This is a mask function which is defined on the Earth's surface and at any given time; in other words, it is a 
function of the angular variable $\gamma=\gamma(\theta,\lambda)$ where $\theta$ is the latitude defined between 
-90° and 90° and $\lambda$ is the longitude, conventionally defined between 0° and 360°. More specifically, the CF
is equal to 1 in the points on Earth's surface (or in  the pixels) where the land is exposed. While CF is equal
to zero in the points (or pixels) which are submerged below the ocean. Mathematically, it can be defined as:

$$
CF(\gamma,t) = 
\begin{cases} 
      1 & \text{if } \hspace{0.5cm} \gamma \text{ is exposed land}\\
      0 & \text{if } \hspace{0.5cm} \gamma \text{ is covered by water}
\end{cases}  
$$


### Results

The project's main script `distribution_acquaterra.py` consists of a main function that calls a set of functions 
specifically designed to elaborate some  SELEN's outputs, specifically the CF and the topography, in order to calculate 
the spatial distribution of Acquaterra, the time evolution of the submerged area of acquaterra and, finally, some 
statistics of acquaterra. These results are saved in an output directory. The detailed description of the input data, 
of the structure and the method used in the project, and of the output files is illustrated in `manual.pdf` file
available in this repository.


## Requirements ##

The main code is verified to properly work on the 3.8, 3.9, 3.10, 3.11, 3.12 and 3.13 python versions.

The dependencies of the code are the following python modules:
- `numpy`
- `matplotlib.pyplot`
## Usage ##

To execute the script of the project, run the following command in your terminal inside the project directory:

```
python3 distribution_acquaterra.py
```

## Some results ##

## Roadmap ##


