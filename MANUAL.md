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
is the longitude, conventionally defined between 0° and 360°. More specifically, the CF
is equal to 1 in the points on Earth's surface (or in  the pixels) where the land is exposed. While CF is equal
to zero in the points (or pixels) which are submerged below the ocean. Mathematically, it can be defined as:

$$
CF(\gamma,t) = 
\begin{cases} 
      1 & \text{if } \hspace{0.5cm} \gamma \text{ is exposed land}\\
      0 & \text{if } \hspace{0.5cm} \gamma \text{ is covered by water}
\end{cases}  
$$

The topography T is also a function of the position on Earth's surface and the time $T=T(\gamma,t)$; and is defined
as the opposite of the so called **sea-level** (SL) which is the height of the sea-surface (or the geoid) with 
respect to the solid earth's surface. As the geoid is a constant gravitational potential surface, both the the topography
and sea-level can be determined in the dry land and in the ocean.


## Data input format


# Method

# Output data and plots