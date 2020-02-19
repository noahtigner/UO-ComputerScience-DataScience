# README #

Apply Douglas-Peucker line simplification algorithm and display 
the before and after version. Python 3. 

This is intended to be a programming exercise near the beginning of 
CIS 211, which spans the end of ACM CS1 and ACM CS2 in the ACM 
curriculum.   It is primarily an exercise in divide-and-conquer 
problem solving using recursion, and secondarily an exercise in 
design of classes and objects.

## Manifest

* geometry.py:  Defines the PolyLine data structure with operations
that include Douglas-Peucker simplification to a given tolerance
* test_geometry.py:  Unit tests for geometry.py
* view_simplify.py:  Visualization of a path and animation of
approximation algorithm
* transform.py: Geometric transformations for display.  Used by
view_simplify
* plot_path.py:  Driver program --- Plot a geometry (.csv) file and
illustrate its simplification.

These files follow a Model-View-Controller scheme.  Package 'geometry'
is in the model component.  'view_simplify' is a corresponding 'view'
component that receives event notifications from the model and manages
the graphical view.  There is no real controller component (no
graphical input), but the driver program (plot_path.py) accepts
keyboard input. 

## Project requirements

Students start with a skeleton version of the simplification method,
which they must complete.  Completing the simplification method
includes generating the event notifications used by the view
component.

## To test

```python3 test_geometry.py```

The student starter code should fail several tests until the the simplify method has been completed. 

## To demonstrate

```python3 plot_path.py data/FoxHollow.csv 600 600 50```

This will simplify a 17 mile path around Eugene from 1502 points
to 61 points while deviating no more than 50 meters from the full
path. Expected output (in addition to graphical display): 

```
Press enter to simplify
Simplified from 1502 points to 61 points
Press enter to dismiss
```


### Who do I talk to? ###

* Developed by Michal Young, michal@cs.uoregon.edu
