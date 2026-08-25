# Administration Guide

## Installation

!!! warning "Recommendation"
    Unless you have a reason to build the container yourself, it is strongly 
    recommended that you download one of the prebuilt containers.

You can install BOLDQC either by downloading one of the [prebuilt 
containers][Download Container], or by [building the container][Building 
Container] manually.

### Downloading the container
There are prebuilt versions of BOLDQC hosted on [GitHub Container
Registry][GHCR]. You can pull the latest version by running

```bash
docker pull ghcr.io/harvard-nrg/boldqc:0.7.1
```

If you are using [Apptainer/Singularity][], you can use the following command
instead

```bash
singularity build boldqc.sif docker://ghcr.io/harvard-nrg/boldqc:0.7.1
```

!!! note "Running with Singularity"
    To run `boldQC.py` with Singularity, you'll need to supply 
    `--pwd /sw/apps/boldqc`

    ```bash
    singularity run --pwd /sw/apps/boldqc boldqc.sif --help
    ```

### Building the container
To build BOLDQC as a container, grab the latest `Dockerfile` from the repository 
and run

```bash
docker build -t boldqc:latest - < Dockerfile
```

After building the container, you should be able to execute `boldQC.py` with docker

```bash
docker run boldqc:latest --help
```

## XNAT Integration
The following section will describe how to integrate BOLDQC into your [XNAT][]
installation by building, installing, and configuring the plugin.

### Building the plugin
Clone the `xnat-1.8` branch from the BOLDQC repository

```bash
git clone -b xnat-1.8 --single-branch https://github.com/harvard-nrg/boldqc
```

XNAT plugins are built using [Gradle][]. Change your working directory into the
cloned repository directory, and compile the plugin

```bash
cd boldqc
./gradlew jar
```

Once the plugin has been successfully compiled, move the resulting `.jar` into 
your XNAT plugins directory

```bash
mv ./build/libs/boldqc-plugin-1.0.0.jar ${XNAT_HOME}/plugins/
```

### Setting up the container
!!! note "Important note"
    Following this documentation section assumes you have successfully 
    [downloaded][Download Container] one of the prebuilt container images,
    or you have [built][Building Container] the container image manually, and 
    you have the container image available from a local Docker daemon 
    service e.g., `unix:///var/run/docker.sock` running on your XNAT server.

To setup the container within [XNAT][], go to `Administer > Plugin Settings >
Images & Commands`, find the BOLDQC container, and click `Add New Command`

You should see a dialog box where you can configure your command. 
Paste the contents from [command.json][]

Now, navigate to your Project home page and click on `Project Settings` in
the `Actions` box. Select `Configure Commands` and enable the new command for
your project

You are now ready to [run the BOLDQC pipeline][Run BOLDQC] from the XNAT user
interface!

[command.json]: https://github.com/harvard-nrg/boldqc/blob/xnat-1.8/command.json
[Apptainer/Singularity]: https://apptainer.org/
[GHCR]: https://ghcr.io/harvard-nrg/boldqc
[Download Container]: #downloading-the-container
[Building Container]: #building-the-container
[XNAT]: https://www.xnat.org
[Gradle]: https://gradle.org/install/
[Run BOLDQC]: ../user/#running-the-pipeline
