Relman: Release Manager
=======================

JIRA automation in a nutshell.

## Installation

There are two ways you can install JIRA workflow on your machine:

* Virtualenv: the application and its dependencies are installed within a
  self-contained python virtualenv.
* System-wide: the application and its dependencies are installed within
  global system directories.

### Virtualenv

For MacOSX or Linux:

    $ sudo easy_install virtualenv

or:

    $ sudo pip install virtualenv

On Ubuntu systems:

    $ sudo apt-get install python-virtualenv

Once the package is installed, you'll want to create your virtualenv:

    $ mkdir releases
    $ cd releases
    $ virtualenv venv

Activate the venv:

    $ source venv/bin/activate

Install the application:

    $ pip install rmt

### System Installation

This will install the application into system directories:

    $ sudo pip install rmt

