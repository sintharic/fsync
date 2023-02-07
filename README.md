fsync
=====

A Python-based backend for version-controlled Cloud / NAS / file synchronization and backup management.
The current version is stable and tested for the features it provides. 
The repository will only be updated in case it provides any significant additions compared to using rsync. 
For now, this is not the case.

Content
-------
In principle, `fsync` is very simple: 
There is only a single function, `sync_directory(...)`, which does all the heavy lifting. 
The rest of the code can be summarised as follows:

- exception handling (otherwise, unexpected errors might interrupt the file transfer and compromise the data), 
- logging (for trouble shooting in case something unexpected does occur),
- a `job` class providing an object-oriented way to interact with the module.
- examples and tests.

Usage
-----
Check out the `test` and `examples` directories to learn how to use the module.
