# B-Splines
 B-Splines is a module for calculating and plotting 2D B-Spline curves. 

<br>

# Requirements and Dependencies
 This module was written for [Python 3.9](https://www.python.org/), although older versions will probably also work fine. However, you need to have the [numpy](https://numpy.org/) and [matplotlib](https://matplotlib.org/) libraries installed for this module to work. 
 If they're not yet present on your machine, open the terminal and use the package manager [pip](https://pip.pypa.io/en/stable/) to install them like this: 

 ```bash
 pip install numpy
 pip install matplotlib
 ```
<br>

# Usage
 To be able to use this module, just put it in your current working directory and create a new Python file.  
 At the beginning of your file, just import the module, for example like this:

 ```python
 import bspline as bsp
 ```
<br>

## Initialization
 Note that you have to initialize before calling any functions. Therefore you have to call the **init()** function like this:

 ```python
 bsp.init(pol_order = 2, interpolations = 1001, control_points = [[1, 3, 5, 9], [2, 4, 1, 5]])
 ```
### Parameters:
  - *pol_order*: the polynomial order of the final B-Spline curve
  - *interpolations*: the number of interpolations for plotting
  - *control_points*: the control points (format: \[\[list: *x_values*\], \[list: *y_values*\]\])

 **Note**: if some of the parameters aren't set, the last values will be uses. If no values have been set so far, standard values will be used.

<br>

# Functions and Methods

## Calculating shape functions:
 With **calc_shape_func()** you can calculate the shape functions of the B-Splines. This function is automatically called by **calc_bslpline()**, so you should only use it if you just want to calculate the shape functions:

 ```python
 bsp.calc_shape_func()
 ```
<br>

## Calculating B-Splines:
 With **calc_bslpline()** you can calculate the B-Spline curve:

 ```python
 bsp.calc_bslpline()
 ```
<br>

## Plotting:
 With **plot_shape_func()**  you can plot the shape functions over all values of the parameter vector u.

 ```python
 bsp.plot_shape_func()
 ```
 ### Parameters: 
 - *order*: the order of the shape functions to be plotted

 <br>
 
 With **plot_bspline()** you can plot the B-Spline curve in a coordinate system with x and y.

 ```python
 bsp.plot_bspline(disp_control_points = True)
 ```

 ### Parameters:
  - *disp_control_points*: boolean that states if the control points and the lines connecting them should be displayed (standard: True)  

<br>

## Showing the plots:
 Note that you have to call the **show()** method after you plotted all the desired plots to be able to see them. As soon as the **show()** method is called, the code is continued only after all plots are closed.   

 ### Example: 
 ```python
 bsp.show()
 ```

<br>
 
 # Example code:
  Here is a full example of how to use the bspline module:
 
 ```python
  import bspline as bsp
  
  
  # Points are stored in this manner: [[x_values], [y_values]]
  points = [[1, 3, 5, 9], [2, 4, 1, 5]]
  
  # Has to be called to initialize.
  bsp.init(pol_order = 2, interpolations = 1001, control_points = points)
  
  # Calculate the shape functions and bspline curve.
  bsp.calc_bslpline()
  
  # Plot the shape functions.
  bsp.plot_shape_func()
  
  # Plot the bspline.
  bsp.plot_bspline()
  
  # Print the influence of all points at a specific value of u.
  bsp.print_influence_at(1.0)
  
  # Show both plots.
  bsp.show()
 ```

<br>

# Info
Author: Luis Brandstätter  
Version: 1.0  
Date: 27.05.21  
