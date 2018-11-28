CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Requirements
 * Configuration
 * Troubleshooting

INTRODUCTION
------------

The Timings Generator generates timing files from a Core Script excel sheet
and the corresponding cue files.

To run the script in command line run '.\timings_generator.py'

REQUIREMENTS
------------

This module requires the following:

 * Python 3.*
 * Pandas (for Python)
 * xlrd (for Python)

CONFIGURATION
-------------

The module has a short menu that allows the user to indicate whether they
want to break the files down to a verse or phrase level and indicate the
book title and chapter number in the file name. There is no configuration. When
run it will replace any timing files already generated at the same location
with the same titles.

TROUBLESHOOTING
---------------
 * Make sure you are running the script with Python 3.
 * Make sure the folders cue_files, core_script, and timings folders exist.
 * If no files appear make sure the cue files and core script are in the correct
   locations.
 * If you switch from phrase to verse make sure to check inside the timing files
   to see whether they have changed.
