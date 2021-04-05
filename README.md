# mde-prototype-python
This repository several prototypes of the Model Data Explorer (MDE) in Python. 
All prototypes were designed to run in an IPython notebook environment and under the Spyder IDE. 
The principal difference among the various prototypes is the library used to (attempt to) render maps:
1. Prototype #1 uses __matplotlib__
2. Prototype #2 uses __folium__
3. Prototype #3 uses __keplergl__
4. Prototype #4 attempts to use __bokeh__

## Requirements and Dependencies

All prototypes depend upon the following libraries:
* Python 3.7
* numpy
* pandas
* openmatrix
* matplotlib
* descartes
* ipympl
* geopandas
* nb_conda
* nb_conda_kernels

## General Background Information

As noted above, the code in these prototypes requires several Python libraries, each of which must be compatible with one another, and all of which must be compatible
with the same "base" version of Python.
The author has determed that, as of the time of writing (March 21, 2021) the latest "base" version of Python that is compatible with _all_ required libraries
is __Python 3.7__.  Some of the required libraries (and specifically _geopandas_) are _not_ compatible with Python 3.8.

Because of the many libraries required and their interdependences, it is pretty much essential to use a "package manager" such as __Anaconda__ to manage
and compose a collection of packages that are compatible and work together successfuly. 
The remaider of this document _assumes_ the use of Anaconda. 
If the reader uses a different package manager, or attempts to "wing it" on his/her own, the author explicitly disclaims any responsibility for any problems 
he/she might encounter. _Caveat emptor._

## Create an Environment in Which to Run Each Prototype or Set of Prototypes

Because of the subtle interdependencies among all the libraries required to run each prototype, I strongly recommend that _you create a dedicated Anaconda environment
in which to run each prototype (or group of prototypes) that depend(s) upon a particular set of libraries_.

### Environment for Prototype #1

The following defines a "baseline" environment; it also fully defines the environment required to run Prototype #1.

1. Open __Anaconda Navigator__ (hereinafter "AC") and click the _Environments_ button in the left-hand window pane. 
2. Click the _Create_ button at the bottom of the AC window to create an Anaconda _environment_ for this project, and give it a suitable name For reasons that will quickly become apparent, the author has chosen to call his environment __base_py_37_omx_geop__. 
3. Use the combo-box to the left of the _Channels_ button to select _Not installed_ option to search for packages that aren't (yet) part of your environment.
4. Search for the __numpy__ library by entering "numpy" into the search box. 
5. A list of libraries matching "numpy" (or upon which "numpy") is dependent will be displayed. 
6. Click the box to the left of "numpy" to select it.
7. Then click the green _Apply_ button at the lower right-hand corner of the screen. This will cause Anaconda to search for all packages on which the selected package depends.
8. When the search has completed, Anaconda will display a dialog box with the complete list of modules that need to be installed. Click the green _Apply_ button in the dialog box to install __numpy__ and all its dependencies.
9. Repeat Steps 4 through 8 for the following libraries:
    1. matplotlib
    2. descartes
    3. ipympl
    4. geopandas
    5. nb_conda
    6. nb_conda_kernels
    7. geopandas
10. The __openmatrix__ package must be installed _manually_; it isn't used widely enough to be "known" to Anaconda:
    1. Use the Windows __Start__ menu to launch an "Anaconda prompt" (i.e., "command box").
    2. Swich to the environment for this project by entering the command __conda activate base_py_37_omx_geop__ (or whatever your environment name is).
    3. Enter the command __python -m pip install openmatrix__.

### Environment for Prototype #2

Using the "baseline" environment as a starting point, use __python - m pip__ to install the __folium__ library.

### Environment for Prototype #3

Using the "baseline" environment as starting point, use __python -m pip__ to install the __keplergl__ library.
Note: I have found that python _must_ be run in __Administrator mode__ in order for the installation of the keplergl library to run to completion successfully.

### Environment for Prototype #4

Using the "baseline" environment as a starting point, use __python - m pip__ to install the __bokeh__ library.

## Additional Background Information

Installing the __openmatrix__ package will auto-install the __tables__ (a.k.a. PyTables) library. 
The __geopandas__ package requires the __descartes__ and __ipympl__ packages in order to render geographic visualizations ("maps"). 
The __matplotlib__ library requires the __nb_conda__ and __nb_conda_kernels__ packages in order to render charts of any kind in an IPython notebook.

## Prototype #1

This prototype uses the __matplotlib__ library to render maps.
It is the most successful prototype to date (March 29, 2021), as it is able to 
* Render a map of all 5,839 TAZes in less than 4 wall-clock seconds, and
* Render a map of all 199,623 links in the model network in less than 19 wall-clock seconds.

## Prototype #2

This prototype is an attempt to use the __folium__ library to render maps.

The __folium__ library was able to generate a map of the TAZes in around 23 wall-clock seconds, it required 56 seconds to render the
model network links. Although rendering of the latter was _apparently_ successful, the notebook in which the map was generated
crashed shortly thereafter with an out-of-memory error losing all previous work and rendering subsequent work impossible. (This 
was observed when running the prototype on an unloaded desktop PC with 6 GB of RAM.)

## Prototype #3

This prototype is an attempt to use the __keplergl__ library to render maps.

While __kelpergl__ was able to render a map of the TAZes in less than 6 wall-clock seconds, it was was not able to render the model network links at all. 
An attempt to do so only produced a "blank map canvas".(Neither the IPython notebook containing the prototype code nor the IPython
kernel running the notebook crashed or hung, however, so subsequent work was possible.

## Prototype #4

This prototype is an attempt to use the __bokeh__ library to render maps.

This prototype was able to render a map of all the model links in just under 18 wall-clock seconds. Getting the prototype to render a map of the TAZes is a work-in-progress.
The __bokeh__ library can only render a "map" from a geopandas data frame that has been suitably "post-processed". That is to say, bokeh has no native understanding of the
"geometry" column of a geopandas data frame: it can only work with raw 'x' and 'y' coordinate values. Data frame columns for 'x' and 'y' values can be created trivially
for point geometry features. For lines, mulit-lines, polygons, and multipolygons more work is required. The python module "geopandas_2_bokeh_tenkanan.py" 
by Hennrikki Tenkanen, which has been copied into this repository seems to "do the job" correctly for lines / multi-lines (e.g., the model links). It, however, 
hasn't yet been shown to work for polygons or multi-polygons (e.g., the TAZes).

<hr/>

Respectfully submitted,  
B. Krepp, attending metaphysician  
Repository created: 9th day of the 2nd month of the Iron Ox Year 2148 (22 March 2021)
