# Setux

Setux is a Python framework to install/deploy/maintain local or remote hosts.

## Abstract

Pure Python
No conf
Lib / Framework


## Usage

### Python

    import setux

### REPL

    $ setux

### CLI

    $ setux command target

## About

This is a meta package including all the packages needed for setux to be functionnal.

### setux [core](https://pypi.org/project/setux_core)

Abstract base classes for all other packages.

### setux [distros](https://pypi.org/project/setux_distros)

core.distro.Distro implementations

Supported OSs (Debian, FreeBSD)

### setux [targets](https://pypi.org/project/setux_targets)

core.target.Target implementations

Connection to the target machine (Local, SSH)

### setux [managers](https://pypi.org/project/setux_managers)

core.manage.Manager implementations

Resources managers (Packages, Services)

### setux [mappings](https://pypi.org/project/setux_mappings)

core.mapping.Mapping implementations

Mapping resources names (Packages, Service)

### setux [modules](https://pypi.org/project/setux_modules)

core.module.Module implementations

User defined functionality 

### setux [logger](https://pypi.org/project/setux_logger)

Default logger


## Additional packages

### setux [REPL](https://pypi.org/project/setux-repl)

Rudimentary Setux REPL / CLI

Note that setux is mainly intended to be used as a Python framework.

### setux [PLUS](https://pypi.org/project/setux-plus)

Augmented Setux distribution

Additional implementations of core's abstract classes.


## Install

    pip install setux

Note : Additional Setux packages install Setux as a dependency.

### Requirements

- Python 3.6+
- Pip
- ssh
- rsync

