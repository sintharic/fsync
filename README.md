fsync
=====

A Python-based backend for version-controlled Cloud / NAS / File Backup management.

Use cases
---------
Contrary to typical Cloud synchronization, this library is (by default) set up for one-way synchronization: 
External changes to the destination folder are not automatically pushed to the local folder, unless you explicitly set up the reverse sync job. 

Contrary to most back-up and mirroring software solutions, the files are copied to the destination folder in a literal way. 
Most back-up solution compress the files and store them in a format that is only readable by the same software.

Content
-------
In principle, `fsync` is very simple. 
There is a single function `sync_directory`, which does all the heavy lifting. 
The rest is just can be summarised as follows:

- exception handling (otherwise, unexpected errors might interrupt the file transfer and compromise the data), 
- logging (for trouble shooting in case something unexpected does occur),
- a `job` class providing an object-oriented way to interact with the module.
- examples and tests.

Usage
-----
Check out the `test` and `examples` directories to learn how to use the module.
