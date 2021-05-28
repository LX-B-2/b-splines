"""
B-splines
-----------------------------
CAMPP HA - Exercise Sheet 6 

This script can calculate and plot 2D b-splines and some 
of their properties based on user parameters.
-----------------------------
Author: Luis Brandstätter
Version: 1.0
Date: 26.05.21 
"""

import matplotlib.pyplot as plt
import numpy as np


# User parameters (assigned values are an example, to be changed with init() function): 

POL_ORDER = 2               # desired polynomial order of the bspline
INTERPOLATIONS = 1001       # number of interpolations for plotting

CONTROL_POINTS = [[1, 3, 5, 9], [2, 4, 1, 5]]       # list of control points ([[x_values], [y_values]])



_NUM_CONTROL_POINTS = len(CONTROL_POINTS[0])        # number of control points



#---------------------------------program structure-----------------------------------#

# Constants:
class Const():
    """Contains the constant values of this script."""

    n: int      # nr. of shape functions
    k: int      # order of shape functions
    p: int      # polynomial degree
    m: int      # size of the knot vector

    def __str__(self) -> str:
        return "consts: n = %d, k = %d, p = %d, m = %d" % (self.n, self.k, self.p, self.m)
    
    def __init__(self) -> None:
        self.n = 0
        self.p = 0
        self.k = 0
        self.m = 0

    def set_all(self, _NUM_CONTROL_POINTS, POL_ORDER) -> None:
        self.n = _NUM_CONTROL_POINTS - 1
        self.p = POL_ORDER
        self.k = self.p + 1
        self.m = self.n + 1 + self.k


t: list         # knot vector

u: list         # parameter vector

__i_max: int    # max num of shape functions in each iteration (will be changed in the course of this program)

x: list         # x values for later plots

curve: list     # this is where the bspline curve will be stored later



N = {}          # shape functions will be stored in this dict

consts = Const()    # constants, to be set


#--------------------------necessary functions for later use--------------------------#

def __set_kont_vector(t_1 = 0):
    """Calculates and sets the knot vector t."""

    global t

    t = []

    for i in range(consts.m):
        if (i < consts.k):
            t.append(t_1)
        elif (consts.k <= i <= consts.n):
            t.append(i - consts.k + 1)
        elif (i > consts.k):
            t.append(consts.n - consts.k + 2)


def __set_param_vector():
    """Sets the parameter vector u."""

    global u

    u = np.linspace(0, ((consts.n + 1) - (consts.k - 1)), INTERPOLATIONS)


def calc_shape_func(__k = 1):
    """
    Calculates the shape functions (according to scrpit CAMPP 2 page 72) 
    and saves them to the above defined dict `N`. 
    This function is called by `calc_bspline()` but can also be called 
    manually ahead of time (e.g. if you want to only calculate and display 
    the shape functions and not the bezier curve as well).
    """

    global N, __i_max

    # calculate __i_max shape functions for the current level
    for i in range(__i_max):
        if(__k == 1):     # base case: first order shape funcitons
            N["N%d%d" % (i, __k)] = []        # define entry "N_i1" as a list

            # fill first order shape functions with ones or zeros according to the definitions
            for x in u:
                if(t[i] <= x < t[i+1]):        # <-- creates numerical instability at the end of last curve, corrected at end of loop
                    N["N%d%d" % (i, __k)].append(1)
                else:
                    N["N%d%d" % (i, __k)].append(0)
        
        else:
            # catch all the possible sources for division by zero and ignore the according terms
            if (t[i+__k-1]-t[i] == 0 and t[i+__k]-t[i+1] == 0):
                # shape function is zero for all values of u
                N["N%d%d" % (i, __k)] = np.zeros(len(u))

            elif (t[i+__k-1]-t[i] == 0):
                # use only second summand
                N["N%d%d" % (i, __k)] = np.divide(np.multiply(np.subtract(t[i+__k], u), N["N%d%d" % (i+1, __k-1)]), t[i+__k]-t[i+1])

            elif (t[i+__k]-t[i+1] == 0):
                # use only first summand
                N["N%d%d" % (i, __k)] = np.divide(np.multiply(np.subtract(u, t[i]), N["N%d%d" % (i, __k-1)]), t[i+__k-1]-t[i])

            else:
                first = np.divide(np.multiply(np.subtract(u, t[i]), N["N%d%d" % (i, __k-1)]), t[i+__k-1]-t[i])
                second = np.divide(np.multiply(np.subtract(t[i+__k], u), N["N%d%d" % (i+1, __k-1)]), t[i+__k]-t[i+1])
                N["N%d%d" % (i, __k)] = np.add(first, second)
    
        # clean up numerical instability at the end of the last non-zero curve
        if (N["N%d%d" % (i, __k)][len(u)-2] > 0.7 and N["N%d%d" % (i, __k)][len(u)-1] == 0):
            N["N%d%d" % (i, __k)][len(u)-1] = 1.0
    
    # abort condition
    if (__k == consts.k):
        return
    
    # reduce __i_max (because next order of functions will have one function less)
    __i_max = __i_max-1

    # recursive call
    calc_shape_func(__k = __k+1)


def __findFirst(list, value):
    """
    Returns the first index of `value` in `list`.

    Parameters
    ----------
    list : list
        The list to be serched trough.
    
    value: any
        The element to be looked for.
    """

    for i in range(len(list)):
        if(list[i] >= value):
            return i
    return -1


def plot_shape_func(order = None):
    """
    This function plots all the shape functions of order `order`.

    Parameters
    ----------
    order : int
        The order of the shape functions to be plotted (standard: highest possible).
    """
    
    if (order == None):
        order = consts.k

    # plot as new figure
    plt.figure()
    plt.suptitle("shape functions of order %d" % order)
    plt.xlabel("u")
    plt.ylabel("Ni%d"%order)
    plt.grid()

    # add shape functions
    for i in range(consts.n+consts.k-order+1):
        plt.plot(x, N["N%d%d" % (i, order)])


def __set_x_values():
    """Sets the x values for later use in plots."""

    global x

    x = np.linspace(0, t[len(t)-1], INTERPOLATIONS)


def print_influence_at(value):
    """
    Prints the influence of all points at the first instance of `value` 
    in the global parameter vector `u`.

    Parameters
    ----------
    value : any
    """

    index = __findFirst(u, value)

    print("\nInfluence of the points on the curve at u = %.4f:" % value)
    for i in range(_NUM_CONTROL_POINTS):
        print("P%d: %.4f" % (i, N["N%d%d" % (i, consts.k)][index]))


def calc_bslpline():
    """Calculates the blspline curve and saves it to global variable `curve`."""

    global curve

    # if N is empty (calc_shape_func() wasn't called before) -> do it now
    if(not N):
        calc_shape_func()

    shape_functions_list = []

    # put all shape functions of order k into a list
    for i in range(__i_max):
        shape_functions_list.append(N["N%d%d" % (i, consts.k)])


    # compute the curve by multiplication with the control points
    curve = np.dot(CONTROL_POINTS, shape_functions_list)


def plot_bspline(disp_control_points = True):
    """
    This function plots the shape functions.

    Parameters:
    ----------
    disp_control_points: bool
        whether to display the control points along with bezier curve (standard: True)
    """

    plt.figure()
    plt.suptitle("bspline curve with control points")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()

    
    # plot the bspline curve (x and y coordinates)
    plt.plot(curve[0], curve[1])

    if (disp_control_points):
        # plot the control points (visualization for the user)
        for i in range(len(CONTROL_POINTS[0])):
            plt.plot(CONTROL_POINTS[0][i], CONTROL_POINTS[1][i], 'x', color = 'red')
            
        # plot lines connecting the controll points (visualization for the user)
        plt.plot(CONTROL_POINTS[0], CONTROL_POINTS[1], color = 'black', linewidth = 0.3)


def show():
    """Shows the created plots."""
    plt.show()


def init(pol_order: int = POL_ORDER, interpolations: int = INTERPOLATIONS, control_points: list[list] = CONTROL_POINTS):
    """
    This function initializes or re-initializes all values (call this function
    at startup or use it to re-initialize with new values). If some of its parameters 
    aren't given, the last given values will be used. If no values have been given so 
    far, standard values will be used.

    Parameters:
    ----------
    pol_order: bool
        polynomial order of the bspline curve
    
    interpolations: int
        No. of interpolations used for plotting
    
    control_points: list[list]
        list of control points written in this manner: [[x_values], [y_values]], where
        the number of points doesn't exceed `pol_order` - 2.
    """

    global consts, __i_max, _NUM_CONTROL_POINTS, POL_ORDER, INTERPOLATIONS, CONTROL_POINTS

    # check for illegal values
    if (pol_order > len(control_points[0])-2):
        raise ValueError("The number of points must be greater than the polynomial order by at least two.")

    # re-set global variables
    POL_ORDER = pol_order

    INTERPOLATIONS = interpolations

    CONTROL_POINTS = control_points

    _NUM_CONTROL_POINTS = len(CONTROL_POINTS[0])

    consts.set_all(_NUM_CONTROL_POINTS = _NUM_CONTROL_POINTS, POL_ORDER = POL_ORDER)

    # set all the other values accordingly
    __set_kont_vector()

    __set_param_vector()

    __i_max = consts.n + consts.k

    __set_x_values()


    # gid settings for the following plots
    plt.rc('grid', linestyle = ":", color = 'black', alpha = 0.3)


    #--------------print the used constants and knot vector for the user---------------#

    print(consts)       # Print consts (the settings)
    print("\nknot vector t: %s" % t)      # Print knot vector t




# The following will be executed only if this file is run standalone.
if __name__ == '__main__':

    print("Hello! This is an example run for this file. " +
    "To use this file as intended, import it from an external file.\n")

    #-----------------------initialize and compute necessary values------------------------#

    init()

    #------------------------calculate and plot the shape functions------------------------#
    
    calc_shape_func()   # call calc_shape_func()
    plot_shape_func()     # plot shape functions for highest possible order k

    #-------------------------influence of the points on the curve-------------------------#

    print_influence_at(1.0) 

    #--------------------------compute and plot the bspline curve--------------------------#

    calc_bslpline()

    plot_bspline()

    show()
