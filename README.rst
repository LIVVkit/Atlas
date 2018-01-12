ISMIP6 Atlas
============

ISMIP6 Atlas is an extension to LIVVkit which can be used to check a project submission's file
structure, variable names and metatdata, and produce a set of standardized diagnostic plots. 


Installation:
-------------

The ISMIP6 Atlas is an extension to `LIVVkit 2.1+ <https://github.com/LIVVkit/LIVVkit>`__, which is
a python 2 and 3 compatible verification and validation toolkit for ice sheet models. LIVVkit is
distributed on both Anaconda and PyPi.  For ease of use, we recommended using `Anaconda
<https://www.continuum.io/downloads>`__/`Miniconda <https://conda.io/docs/install/quick.html>`__ to
satisfy all the dependencies. Alternatively, LIVVkit can be installed using Python pip. 

Anaconda/Miniconda
~~~~~~~~~~~~~~~~~~

Once you have `Anaconda <https://www.continuum.io/downloads>`__/`Miniconda
<https://conda.io/docs/install/quick.html>`__ installed on your system, you can:

* Update an existing Python 2 or 3 ``conda`` environment, adding all the required dependencies, by
  issuing this command:

.. code-block:: bash
    
    conda install -c jhkennedy livvkit

* Create a **new** Python 3 based ``conda`` environment, including all the required dependencies, by
  issuing this command:

.. code-block:: bash
    
    conda create -c jhkennedy --name atlas python=3 livvkit


* Create a new Python 2 based ``conda`` environment, including all the required dependencies, by
  issuing this command:

.. code-block:: bash
    
    conda create -c jhkennedy --name atlas python=2 livvkit

If you've created a new environment, you can activate it by issuing this command:

.. code-block:: bash

    source deactivate && source activate atlas

Python pip
~~~~~~~~~~

Once you have `python and pip
<http://python-guide-pt-br.readthedocs.io/en/latest/starting/installation/>`__ installed on your
system, you'll need to install:

* HDF4
* HDF5
* NetCDF4 with HDF4 support

This will be much easier if you use a package manager (e.g., ``yum``, ``apt``, ``brew``, ``macports``; see `here for
macs <http://alejandrosoto.net/blog/2016/08/16/setting-up-my-mac-for-climate-research/>`__).

Then, install LIVVkit via ``pip``:

.. code-block:: bash

    pip install livvkit

Get the ISMIP6 Atlas
~~~~~~~~~~~~~~~~~~~~

To get the ISMIP6 Atlas, either clone it via github:

.. code-block:: bash

    git clone https://github.com/LIVVkit/Atlas.git
    cd Atlas

Or download and extract the latest version `https://github.com/LIVVkit/Atlas/archive/master.zip`__

Atlas should now be ready to use. 

Usage
-----

*Note: These instructions assume you're current working directory is the directory containing Atlas.
You can work from any directory, but all paths in the JSON configuration files must be edited to
absolute paths or relative paths from your current working directory (not recommended).* 

Atlas is controlled by a JSON configuration file which describes the submission and which ISMIP6
Project the submission is for. A number of example JSON configuration files are contained in the
``examples/`` subdirectory.

For example, using ``examples/GIS-ARC-PISM5KM.json`` would analyze the PISM5KM submission to initMIP
Greenland by the ARC modeling group. The JSON configuration file looks like:

.. code-block:: json

    {
        "initMIP-GIS" : {
            "module" : "atlas.py",
            "data_path" : "data/GrIS/output",
            "experiments": ["init", "ctrl", "asmb"],
            "groups" : {
                "ARC" : ["PISM5KM"]
                }
            }
        }
    }

and is passed to LIVVkit like:  

.. code-block:: bash

    livv -e examples/GIS-ARC-PISM5KM.json -o results --serve

LIVVkit will produce a website detailing the results of the analysis, including the diagnostic
plots, in the ``results`` directory. The ``--serve`` option will fire up a http server and print the
http address viewing the local website in your favorite web browser.  

*Note: See the* `LIVVkit FAQs <https://livvkit.github.io/Docs/faq.html>`__ *for a discussion of the*
``--serve`` *option.* 

The configuration files
-----------------------

The JSON configuration files are structured as a set of nested dictionaries. The outermost dictionary:

.. code-block:: json

    {
        "initMIP-GIS" : {...}
    }

is used to describe which project the submission is for, where the keys are the (case sensitive)
name of the project and used to find an associated project config file in the ``projects/``
subdirectory (``ls projects/`` will give you a list of supported projects). The project config file
describes the variables that should be present, the expected metadata for each variable, and the
plot style for each variable. 

Multiple projects can be analyzed by having multiple project keys in
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
            "data_path" : "data/GrIS/output",
            "experiments": ["init", "ctrl", "asmb"],
            "groups" : {...}
        }
    }

describes what LIVVkit extension module to use for the analysis (always ``"atlas.py"``), a directory
containing the submission data (either a path relative to the working directory, or an absolute
path), the names of the experiments run for that project, and a nested ``"groups"`` dictionary.

The nested ``"groups"`` dictionary:

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


``example/GIS-DMI-PISM0-4.json`` provides an example of analyzing the submission of multiple model
versions (``PISM0``, ``PISM1``, ``PISM2``, ``PISM3``, and ``PISM4``)  by the ``DMI`` group to the initMIP
Greenland project.  

``example/GIS-initMIP.json`` provides an example of analyzing all the group-model(s) submissions to
the initMIP Greenland project, and the file looks like:

.. code-block:: json

    {
        "initMIP-GIS" : {
            "module" : "atlas.py",
            "data_path" : "data/GrIS/output",
            "groups" : {
                "ARC" : ["PISM5KM"],
                "AWI" : ["ISSM1", "ISSM2"],
                "BGC" : ["BISICLES1", "BISICLES2", "BISICLES3"],
                "DMI" : ["PISM0", "PISM1", "PISM2", "PISM3", "PISM4", "PISM5"],
                "ILTS" : ["SICOPOLIS"],
                "ILTSPIK" : ["SICOPOLIS"], 
                "IMAU" : ["IMAUICE1", "IMAUICE2", "IMAUICE1"],
                "JPL" : ["ISSM"],
                "LANL" : ["CISM"],
                "LGGE" : ["ELMER1", "ELMER2"],
                "LSCE" : ["GRISLI"],
                "MIROC" : ["ICIES1", "ICIES2"],
                "MPIM" : ["PISM"],
                "UAF" : ["PISM1", "PISM2", "PISM3", "PISM4", " PISM5", "PISM6"],
                "UCIJPL" : ["ISSM"],
                "ULB" : ["FETISH1", "FETISH2"],
                "VUB" : ["GISM1", "GISM2"]
            },
            "experiments": ["init", "ctrl", "asmb"]
        }
    }


Similarly, ``example/AIS-initMIP.json`` provides an example of analyzing all the group-model(s)
submissions to the initMIP Antarctica project.

Finally, there is also an optional ``strict`` key which can be given in the nested project dictionary like:

.. code-block:: json

    {
        "initMIP-GIS" : {
            "module" : "atlas.py",
            "data_path" : "data/GrIS/output",
            "groups" : {...},
            "experiments": ["init", "ctrl", "asmb"],
            "strict": true
        }
    }

This will prevent Atlas from making "fuzzy" decisions around common submission problems in order to
provide more information in its output website. For example, in the follow on experiments (like ``ctrl``),
modeling groups commonly didn't include the ``init`` submission as the zero-th time step in the model
output as requested. In this case, Atlas will notice there aren't enough time steps in a variable file,
output a Meta Check error indicating missing time step, and either:

* plot the *last* time step in the variable file if there is no ``strict`` key or if ``"strict": false`` is given
* not attempt to plot the variable if ``"strict": true`` is given.

Contributing
------------

Contributions are welcome! When developing the code, please use the `Forking Workflow
<https://www.atlassian.com/git/tutorials/comparing-workflows#forking-workflow>`__ to add
contributions to Atlas (or LIVVkit). 

First, go to the `Atlas github page <https://github.com/LIVVkit/Atlas>`__ and push the Fork button
on the top right of the page.  This will create a fork of LIVVkit on your profile page. Clone the
fork, make your changes, merge them to master branch, and then submit a pull request to our
repository.

If you have any questions, concerns, requests, etc., open an issue in `our issues queue
<https://github.com/LIVVkit/Atlas/issues>`__, and we will help you out.

Contact us
----------

If you would like to suggest features, request tests, discuss contributions,
report bugs, ask questions, or contact us for any reason, use the
`Issue Tracker <https://github.com/LIVVkit/Atlas/issues>`__.

Want to send us a private message?

**Joseph H. Kennedy**

* github: @jhkennedy
* email: `kennedyjh [at] ornl.gov <mailto:kennedyjh@ornl.gov>`__

**Heiko Goelzer** 

* email: `h.goelzer [at] uu.nl <mailto:h.goelzer@uu.nl>`__

