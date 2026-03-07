## Reflection

The Makefile makes the dependency structure of the project explicit in a way that run_all.sh did not. In the bash script, the steps were just listed in order, so it was not clear which files depended on which outputs or why the steps had to run in that sequence. The Makefile shows exactly how the figures, tables, and final paper depend on the input data and Python scripts. This also allows Make to rebuild only the parts of the project that changed instead of rerunning everything. For a new collaborator, reading the Makefile makes it much easier to understand the workflow of the replication project.

