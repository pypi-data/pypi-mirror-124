pl-pull_scp
================================

.. image:: https://img.shields.io/docker/v/fnndsc/pl-pull_scp?sort=semver
    :target: https://hub.docker.com/r/fnndsc/pl-pull_scp

.. image:: https://img.shields.io/github/license/fnndsc/pl-pull_scp
    :target: https://github.com/FNNDSC/pl-pull_scp/blob/master/LICENSE

.. image:: https://github.com/FNNDSC/pl-pull_scp/workflows/ci/badge.svg
    :target: https://github.com/FNNDSC/pl-pull_scp/actions


.. contents:: Table of Contents


Abstract
--------

This plugin application is used to recursively copy data from a remote host into an analysis root node.


Description
-----------

``pull_scp`` is a *ChRIS fs-type* application that produces data for an analysis tree by copying data off a remote host using (recursive) ``scp``.

Of course this assumes that the user executing this plugin has the correct login credentials to access the resource. Credentials are defined in either:

* a hard-coded .env file in the repo/container
* setting appropriate environment variables
* using plugin CLI arguments

Other than login credentials, this plugin also needs a ``filepath`` in the remote user space. All files and directories rooted in this file ``filepath`` are copied into this plugin's ``outputdir``.

Warning
-------

This plugin/app is not considered or purported to be secure! One deployment vector has the login credentials contained within an ``.env`` file in cleartext and copied into the container. Deploying such a container will expose login credentials! For better security, supply login credentials from the CLI or from within environment variables:

.. code:: bash

    export ENVIRONMENT=development
    export SSH_REMOTE_HOST=1.1.1.1
    export SSH_USERNAME=yourname
    export SSH_PASSWORD=yourpassword
    export SSH_KEY_FILEPATH=/usr/local/src/key.pub
    export SCP_DESTINATION_FOLDER=/tmp

Credit
------

Most of the innards of this plugin are lightly adapted from the most excellent paramiko tutorial of Todd Birchard:

* https://hackersandslackers.com/automate-ssh-scp-python-paramiko


Usage
-----

.. code::

        docker run --rm fnndsc/pl-pull_scp pull_scp                     \
            [-h] [--help]                                               \
            [--json]                                                    \
            [--man]                                                     \
            [--meta]                                                    \
            [--savejson <DIR>]                                          \
            [-v <level>] [--verbosity <level>]                          \
            [--version]                                                 \
            [--username <username>]                                     \
            [--password <password>]                                     \
            [--host <hostname>]                                         \
            [--sshPubKeyFile <pubKeyFile>]                              \
            --filepath <filepath>                                       \
            <outputDir>


Arguments
~~~~~~~~~

.. code::

        --filepath <filepath>
        The path in the <hostname>'s filesystem to pull. This is technically
        the only required argument of this plugin. All user specific
        credentials are assumed to be container in the .env file or set in
        environment variables. Note of course that all the credentials can
        be overriden with CLI flags.

        [--username <username>]
        The username in the remote host.

        [--password <password>]
        The <username>'s password to connect to the remote host.

        [--sshPubKeyFile <pubKeyFile>]
        The ssh public key file to use in this session.

        [--host <hostname>]
        The hostname to access.

        [-h] [--help]
        If specified, show help message and exit.

        [--json]
        If specified, show json representation of app and exit.

        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.

        [--savejson <DIR>]
        If specified, save json representation file to DIR and exit.

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number and exit.


Install
~~~~~~~

Installation is either via ``docker`` (recommended) or directly from ``PyPI`` (less recommended).

From docker
^^^^^^^^^^^

.. code:: bash

    docker pull fnndsc/pl-pull_scp

Getting inline help is:

.. code:: bash

    docker run --rm fnndsc/pl-pull_scp pull_scp --man


From PyPI
^^^^^^^^^

.. code:: bash

    pip install pull_scp

For this use case, copy your public key to ``/tmp/key.pub`` and create an environment file ``/tmp/.env`` that either contains your login data/credentials or contains "dummy" data. The ``.env``  _must_ exist for the app to work -- regardless of the validity of its data.

Run
~~~

Since ``docker`` is the recommended usagage deployment, the following instructions are ``docker`` based.

Being an _FS_ plugin, you should specify an output directory using the ``-v`` flag to ``docker run``.


.. code:: bash

    docker run --rm -u $(id -u)                             \
        -v $(pwd)/out:/outgoing                             \
        fnndsc/pl-pull_scp pull_scp                         \
        --username johnnyapple                              \
        --password 'mysecret'                               \
        --host computer.org                                 \
        --sshPubKeyFile ~/.ssh/rsa_pub.key                  \
        --filepath /home/johnnyapple/data                   \
        /outgoing


Development
-----------

Build the Docker container:

.. code:: bash

    docker build -t local/pl-pull_scp .

Run unit tests:

.. code:: bash

    docker run --rm local/pl-pull_scp nosetests

Examples
--------

Using login credentials stored in the container's `.env` file:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All relevant login credentials are stored in ``/tmp/.env`` in the container. Note this method embeds the ``.env`` file in the container where it can be potentially expose credentials!

.. code:: console

    mkdir out && chmod 777 out
    docker run --rm -u $(id -u) --name=pl-pull_scp              \
                -v $PWD/out:/outgoing                           \
                -it                                             \
                local/pl-pull_scp pull_scp -v 1                 \
                --filepath /home/rudolphpienaar/Desktop         \
                outgoing

    10-15-2021 16:25:38 | INFO: /usr/local/src/key.pub uploaded to 192.168.1.216

                 _ _
                | | |
     _ __  _   _| | |  ___  ___ _ __
    | '_ \| | | | | | / __|/ __| '_ \
    | |_) | |_| | | | \__ \ (__| |_) |
    | .__/ \__,_|_|_| |___/\___| .__/
    | |           ______       | |
    |_|          |______|      |_|

    Version: X.Y.Z
    10-15-2021 16:25:38 | INFO: (remote): du -ksh /home/rudolphpienaar/Desktop: 142M	/home/  rudolphpienaar/Desktop
    10-15-2021 16:25:39 | INFO: Pulling rudolphpienaar@192.168.1.216:/home/rudolphpienaar/Desktop...
    10-15-2021 16:25:53 | INFO: Remote contents pulled to /outgoing
    10-15-2021 16:25:53 | INFO: (NOTE: if running in a container, and doing a volume mapping,
                                the destination dir name might not match the host dirname!)
    10-15-2021 16:25:53 | INFO: (local): du -ksh /outgoing: 142M	/outgoing

Using login credentials from the CLI:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Credentials are supplied at run time. Contents of ``/tmp/.env`` are not used.

.. code:: console

    docker run --rm -u $(id -u) --name=pl-pull_scp          \
                -v $PWD/out:/outgoing                       \
                -it                                         \
                local/pl-pull_scp pull_scp -v 1             \
                --filepath /home/chris/Pictures             \
                --host 192.168.1.200                        \
                --username chris                            \
                --password XXXXXXXXXXX                      \
                /outgoing
    10-15-2021 17:05:13 | INFO: /usr/local/src/key.pub uploaded to 192.168.1.200

                 _ _
                | | |
     _ __  _   _| | |  ___  ___ _ __
    | '_ \| | | | | | / __|/ __| '_ \
    | |_) | |_| | | | \__ \ (__| |_) |
    | .__/ \__,_|_|_| |___/\___| .__/
    | |           ______       | |
    |_|          |______|      |_|

    Version: X.Y.Z
    10-15-2021 17:05:14 | INFO: (remote): du -ksh /home/chris/Pictures: 81M	/home/chris/Pictures
    10-15-2021 17:05:14 | INFO: Pulling chris@192.168.1.200:/home/chris/Pictures...
    10-15-2021 17:06:01 | INFO: Remote contents pulled to /outgoing
    10-15-2021 17:06:01 | INFO: (NOTE: if running in a container, and doing a volume mapping,
                                the destination dir name might not match the host dirname!)
    10-15-2021 17:06:01 | INFO: (local): du -ksh /outgoing: 156M	/outgoing

(note that in this example the ``local`` directory is larger than the ``remote``. This occurs when the remote directory contains symbolic links -- each symbolic link is actually translated into the target file when pulled)

_-30-_

.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co
