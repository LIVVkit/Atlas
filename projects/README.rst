Adding a new  project
=====================

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
            "timestep" : {"init": 0, "ctrl": 20, "asmb": 20},
            "colormap" : "...",
            "lmode" : 0,
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
            },
            ...
        }
    }

where there are nested dictionaries for each 2D variables, describing the plotting style for
matplotlib and expected metadata, and a final nested scalar dictionary containing a set of
dictionaries for each scalar variable which describe each variables expected metadata. 



