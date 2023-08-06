``kokiy`` contains utilities to work on 2D and 3D structured grids. Grid can be either cartesian plane (``CartShell``) or axi-cylindrical extrusion from a x-r spline (``AxiShell``). ``ThickShell`` are 3D shells built by extruding any of available 2d objects.


Main features include:

* create 2D and 3D structured grids (including axi-cylindrical objects)
* interpolate a solution
* average solution over a direction
* dump shells for fields visualization in `ParaView <https://www.paraview.org/>`_
* export mesh in any format available in `yamio <https://pypi.org/project/yamio/>`_ (e.g. ``hip``-friendly ``.hdf5``, ``xdfm``, ``dolfin-xml``)
* export ``.geo`` files for visualization with `tiny-3d-engine <https://pypi.org/project/tiny-3d-engine/>`_



Installation
------------

Install with


.. code-block:: bash

    pip install kokiy
