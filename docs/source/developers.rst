Developer documentation
=======================
.. _XNAT: https://xnat.org
.. _command.json: https://github.com/harvard-nrg/boldqc/blob/xnat-1.8/command.json
.. _Gradle: https://gradle.org/install/

Installation
------------
At the moment, the only supported way to install BOLDQC is `within a container <#building-a-container>`_.

downloading a container
^^^^^^^^^^^^^^^^^^^^^^^
There are prebuilt versions of BOLDQC on `Docker Hub <https://hub.docker.com/repository/docker/neuroinformatics/boldqc>`_. You can pull the latest version by running ::

    docker pull neuroinformatics/boldqc

or you can pull a specific version e.g., ``0.1.0`` by running ::

    docker pull neuroinformatics/boldqc:0.1.0
    
building a container
^^^^^^^^^^^^^^^^^^^^
To build BOLDQC as a container, grab the latest `Dockerfile <https://github.com/harvard-nrg/boldqc/blob/main/Dockerfile>`_ from the repository and run ::

    docker build -t boldqc:latest - < Dockerfile

Now you can run ``boldQC.py``---which is the default ``ENTRYPOINT``---using ``docker run`` ::

    docker run boldqc:latest --help

.. note::
   You can also convert the BOLDQC Docker image into a Singularity image, 
   however to run ``boldQC.py`` you'll need to supply ``--pwd /sw/apps/boldqc`` ::

       singularity run --pwd /sw/apps/boldqc boldqc.sif --help

XNAT Installation
-----------------
The following section will describe how to build and configure BOLDQC as a `XNAT`_ plugin.

building the plugin
^^^^^^^^^^^^^^^^^^^
Clone the ``xnat-1.8`` branch from the ``github.com/harvard-nrg/boldqc`` 
repository ::

    git clone -b xnat-1.8 --single-branch https://github.com/harvard-nrg/boldqc

Change into the repository directory and compile the plugin using `Gradle`_ ::

    ./gradlew jar

Once the plugin has been compiled, move the resulting ``.jar`` into your XNAT plugins directory ::

    mv ./build/libs/boldqc-plugin-1.0.0.jar ${XNAT_HOME}/plugins/
