# mde-prototype-python
Prototyping the Model Data Explorer (MDE) in Python

## Background

The code in this prototype requires several Python libraries, each of which must be compatible with one another, and all of which must be compatible with the same "base" version of Python. The author has determed that, as of the time of writing (March 21, 2021) the latest "base" version of Python that is compatible with all required libraries is __Python 3.7__.  All required libraries (and specifically _geopandas_) is not compatible with Python 3.8.

Because of the many libraries required and their interdependences, it is pretty much essential to use a "package" manager such as __Anaconda__ to manage and compose a collection of packages that are compatible and work together successfuly. The remaider of this document _assumes_ the use of Anaconda. If the reader uses a different package manager, or attempts to "wing it" on his/her own, the author explicitly disclaims any responsibility for any problems he/she might encounter.

## Create an Environment in Which to Run the Prototype

1. Open __Anaconda Navigator__ (hereinafter "AC") and click the _Environments_ button in the left-hand window pane. 
2. Click the _Create_ button at the bottom of the AC window to create an Anaconda _environment_ for this project, and give it a suitable name For reasons that will quickly become apparent, I've chosen to call my environment __base_py_37_omx_geop__. 
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

## Additional Background Information

Installing the __openmatrix__ package will auto-install the __tables__ (a.k.a. PyTables) library. The __geopandas__ package requires the __descartes__ and __ipympl__ packages in order to render geographic visualizations ("maps"). The __matplotlib__ library requires the __nb_conda__ and __nb_conda_kernels__ packages in order to render charts of any kind in an IPython notebook.
