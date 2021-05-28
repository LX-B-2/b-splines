"""
B-Splines
-----------------------------
CAMPP HA - Exercise Sheet 6 

This script is an example of how to use the bspline python file.
-----------------------------
Author: Luis Brandstätter
Version: 1.0
Date: 26.05.21 
"""

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

