fsync
=====

A Python-based backend for version-controlled Cloud / NAS / File Backup management.

Use cases
---------
Do you often acquire data on one device but work with the data on a different device? 
This not only happens with scientific computations, but also with creative work like video and audio production, for example.
In that case, the established solutions do not provide exactly what you need.

Contrary to a typical (potentially expensive) Cloud solution, this library is (by default) set up for one-way synchronization: 
External changes to the destination folder are not automatically pushed to the local folder, unless you explicitly set up the reverse sync job. 

Contrary to most back-up and mirroring software solutions, the files are copied to the destination folder in a literal way, which allows you to immediately start working with them. 
(A lot of back-up solutions compress the files and store them in a format that is only readable by the same software.)

Consequently, `fsync` is most useful in a local network to seemlessly synchronize and work with the same data on multiple devices.
It may also include simple backups, if those backups are accessed frequently enough to justify uncompressed storage.
For example, this makes it very easy to roll back an individual file to a previous version.

Content
-------
In principle, `fsync` is very simple. 
There is only a single function, `sync_directory(...)`, which does all the heavy lifting. 
The rest of the code can be summarised as follows:

- exception handling (otherwise, unexpected errors might interrupt the file transfer and compromise the data), 
- logging (for trouble shooting in case something unexpected does occur),
- a `job` class providing an object-oriented way to interact with the module.
- examples and tests.

Usage
-----
Check out the `test` and `examples` directories to learn how to use the module.
