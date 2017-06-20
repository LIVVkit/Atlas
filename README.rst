ISMIP6 Atlas
============

ISMIP6 Atlas is an extension to LIVVkit which can be used to check a project submission's file
structure, variable names and metatdata, and produce a set of standardized diagnostic plots. 


Installation:
-------------

The ISMIP6 Atlas is an extension to `LIVVkit 2.1+ <https://github.com/LIVVkit/LIVVkit>`__, which is
a python 2 and 3 compatible verification and validation toolkit for ice sheet models. LIVVkit is
distributed on Both PyPi and Anaconda, and can be installed by following its `installation
instructions <>`__. 

In addition to LIVVkit, Atlas requires:

* NCL

For ease of use, we recommended using Anaconda/Miniconda to satisfy all the dependencies and setup an ISMIP6 Atlas environment from one
of the provided YAML environment descriptions:

* `atlas_py3.yml`: (Recommended) A Python 3 based `conda` environment, including all the required dependencies.
  Create the environment by issuing these commands:

.. code-block:: bash
    
    conda create -f atlas_py3.yml


* `atlas_py2.yml`: A Python 2 based `conda` environment, including all the required dependencies.
  Create the environment by issuing these commands:

.. code-block:: bash
    
    conda create -f atlas_py2.yml

Once the environment is setup, activate it by issuing this command:

.. code-block:: bash

    source deactivate && source activate Atlas


Usage
-----

.. note:: 
    
    These instructions assume you're current working directory is the directory containing Atlas.
    You can work from any directory, but all paths in the JSON configuration files must be edited to
    absolute paths or relative paths from your current working directory (not recommended). 

Atlas is controlled by a JSON configuration file which describes the submission, which ISMIP6 Project
the submission is for, and the NCL plot script used for the diagnostic plots. For example, to test
the PISM5KM submission to initMIP Greenland by the ARC modeling group, the JSON file would look
like:

.. code-block:: json

    {
        "initMIP-GIS" : {
            "module" : "atlas.py",
            "plot_script" : "atlas.ncl",
            "data_path" : "data/GrIS/output",
            "experiments": ["init", "ctrl", "asmb"],
            "groups" : {
                "ARC" : {
                    "models" : ["PISM5KM"]
                }
            }
        }
    }

as seen in `atlas-ARC-PISM5KM.json`. This JSON configuration file would then be passed to LIVVkit
like:  

.. code-block:: bash

    livv -V atlas.json -o results

and LIVVkit would produce an website detailing the results of the analysis and the diagnositic plots
in the `results` directory. This website can then be viewed locally in your favorite web browser. 


The configuration files
-----------------------

The JSON configuration files are structured as a set of nested dictionaries. The outermost dictionary:

.. code-block:: json

    {
        "initMIP-GIS" : {...}
    }

is used to describe which project the submission is for, where the keys are the (case sensitive)
name of the project. Atlas will use this name to find an associated project JSON config file which
describes the variables that should be present, the expected metadata for each variable, and the
plot style for each variable. Multiple projects can be analyzed by having multiple project keys in
this dictionary. For example:

.. code-block:: json

    {
        "initMIP-GIS" : {...},
        "initMIP-AIS" : {...}
    }

Will analyze initMIP submission for both Greenland and Antarctica. The nested project dictionary:

.. code-block:: json

    {
        "initMIP-GIS" : {
            "module" : "atlas.py",
            "plot_script" : "atlas.ncl",
            "data_path" : "data/GrIS/output",
            "experiments": ["init", "ctrl", "asmb"],
            "groups" : {...}
        }
    }

describes what LIVVkit extension module to use for the analysis (always `"atlas.py"`), which NCL
plot script to use for the diagnostic plots (`"atlas.ncl"` is the default), a directory containing
the submission data (either a path relative to the working directory, or an absolute path), the
names of the experiments run for that project, and a nested `"groups"` dictionary. 

The nested `nested `"groups"` dictionary: 

.. code-block:: json

    {
        "initMIP-GIS" : {
            ...,
            "groups" : {
                "ARC" : ["PISM5KM"]
            }
        }
    }

Contains the name of the modeling group, and a list of the model submissions to analyze. Like with
the projects, multiple groups can be analyzed at the same time by adding them to this dictionary:

.. code-block:: json

    {
        "initMIP-GIS" : {
            ...,
            "groups" : {
                "ARC" : ["PISM5KM"],
                "DMI" : ["PISM0, PISM1"]
            }
        }
    }


Adding a new  project
---------------------

The projects currently available for analysis have a JSON configuration file in the `projects`
subdirectory:

* `initMIP-GIS.json`
* `initMIP-AIS.json`

To add a new project, you'll need to create a JSON file for that project containing nested
dictionaries of the form:

.. code-block:: json

    {
        "VAR" : {
            "meta" : {
                "dims" : [...],
                "type" : "...",
                "standard_name" : "...",
                "units" : "..."
            },
            "timestep" : {"init": 0., "ctrl": 20, "asmb": 20},
            "palette" : "...",
            "levelmode" : 0,
            "lmin" : 0,
            "lmax" : 0,
            "lstep": 0,
            "levels" : "(/.../)"
        },
        "scalar" : {
            "VAR" : {
                    "meta" : {
                        "dims" : [...],
                        "type" : "...",
                        "standard_name" : "...",
                        "units" : "..."
                }
            }
        }
    }

where there are nested dictionaries for each 2D variables, describing the plotting style and
expected metadata, and a final nested scalar dictionary containing a set of nested dictionaries for
each scalar variable which describe each variables expected metadata. 


Contributing
------------




Contact us
----------


