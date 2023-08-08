##User waypoints

To import user waypoints into the GTN750, they must be all stored in one file that fulfills the following requirements:

- name: 'user.wpt'
- each waypoint in this file has its own line
- The GTN can store xxx waypoints
- waypoints are defined with four columns, separated by a ','.
The columns are:
   - **Waypoint ID**: max. 6 alphanumeric characters (all UPPERCASE). Names can probably be used multiple times, but this is not recommended. This ID is the one that pilot will see in their maps during flight.
   - **Waypoint comment**: max. 25 alphanumeric characters (all UPPERCASE). The comment can only be seen by the pilots when looking at the list of user waypoints. Not that easy to access when actually following a flightplan. The comments do not need to be unique either.
   - **Latitude** in decimal degrees. e.g., '67.503777168'. Number of decimal places is (probably) not limited.
   - **Longitude** in decimal degrees. e.g., '-133.7815498'. Number of decimal places is (probably) not limited.
- Waypoints cannot be closer than 0.001° to each other (111m). If this happens, the GTN750 will only import the first waypoint with 'this' coordinate 
  and the second one, that is in the 111m-vicinity will be ignored! This is especially relevant to consider when flying survey grids --> lines need to 
  be far enough apart._ Reason: The userwpts are only single points with a name. A FPL instead puts different coordinates into an order, but with NO name. The name of these ordered coordinates will be assigned by the closesst userwpt to that coordinate. Now here comes the problem: The FLP coordinate is in DMM format with only one decimal accuracy. Hence the name of this coordinate will come of the closest userwpt in a 0.001° radius. Closer lines can really mess up the naming of the points._
- User waypoints that were stored in the GTN stay in there until they are manually deleted. So creating and importing waypoints (via a new user.wpt) at a later point in time, might also generate this issue. Those that are already in the GTN will not be overwritten!
NOTE: The distance value of 0.001°/111 m was taken from the GTN750 manual. However, we already faced some issues with points that were 160 m apart. So be careful.
Practical Implications:
   - It is not possible to upload flightplans of an identical area with different height settings to account for high/low cloud ceiling
   - It is not possible to upload overlapping flightplans if the final linespacing is lower than 0.001°
   - Remove all existing user waypoints after each flight day to avoid issues with identical name / too close waypoints.
- the order of the waypoints is not important
- example user.wpt:
03712A,037DTTSIIGEHTCHIC020750M12A,67.491477146,-133.87411029
03712B,037DTTSIIGEHTCHIC020750M12B,67.489548245,-133.65816177
03801A,038LARCHESINUVIK011000M01A,67.914663523,-133.62897633
03801B,038LARCHESINUVIK011000M01B,67.914663523,-133.45728749
03802A,038LARCHESINUVIK011000M02A,67.906953613,-133.4572875

##Flightplans

For the GTN750 to be able to read prepared flightplans, they must fulfil certain (format) requirements:
- stored as .gfp (Garmin flightplan)
- coordinates must be in DMM format
- Syntax is the following:
  FPN/RI:F:N67302W133469:F:N67261W133470:F:N67260W133449:F:N67302W133448
  - always start with 'FPN/RI'
  - each coordinate is prefaced with ':F:'
  - coordinates are in Lat/Lon order
     - Lat prefaced with N or S; followed by exactly five digits in DMM: 67° 30.2' N becomes N67302
     - Lon prefaced with E or W; followed by exactly six digits in DMM: 133° 46.9' W becomes W133469
- .gfp-file is allowed to have only one line! The entire flightplan needs to be in this long line. Make sure, there is no empty new line.
- NOTE: the import of a .gfp file created in a unix operating system failed, only windows worked. (Line ending problem?)
- all .gfp-files need to be collected in one folder named 'FPL'
- The GTN750 can store up to 100 flightplans (?) --> this needs to be verified.
- there are possibilities to add more complex information to the flightplan (e.g. airports, runways, landing approaches, etc... --> see manual), but generally not necessary. (the simpler, the better ;) )

The coordinates of a .gfp-file do not have names/IDs. If you import a .gfp-file to the GTN750 without previously importing the exact user waypoints first, the system will give these coordinates a generic ID along the lines of USR001, USR002, etc... 
If you want to avoid this, make sure that the user waypoints are imported before the flightplans are (the .gfp-files).

Importing the flightplans to the Garmin:
1) import user.wpt first
2) import the flightplans

Explanantion: see above

The script '01_xxx' reads all '*_user.wpt'-files in a directory and creates a flightplan for each of them. The new name is then '*_fpl.gfp'.
Originally, when exported from MACS-MissionPlanner (vXX.XX), the waypoint-IDs are named e.g., 'FL02_A' or FL05_B', numbered consecutively in the order they were 
in the MACS-MissionPlanner .xml-file.(TODO @Tabea: explain this better). And the comments are based on the names visible in this upper left panel. 
If you do not change the order of the flightlines, the IDs and comments should be in the same numbering order. HOWEVER: for each mission, the IDs will start at FL01_A again.
When importing many waypoints into the GTN, this will become very confusing, and complicate communication with the pilots. We therefore recommend renaming the waypoints
and creating unique IDs and comments.
Currently, this is done via the script xxx. It creates an intermediate file ('*_user_renamed.wpt') for each mission, where the ID and comment are updated based on 
the NAME of the original '*_user.wpt' file. We therefore suggest the following naming conventions for missions:

004_some-name --> 004 being the internally given ID.
The following files should then ideally be named like this:

- MACS-MissionPlanner file: 004_some-name.xml
- user waypoint file: 004_some-name_user.wpt (export via MACS-MissionPlanner)
- geojson (if desired): 004_some-name.geojson (export via MACS-MissionPlanner)

If you adhere to this naming scheme, the scripts will generate the following files:

- 004_some-name_user_renamed.wpt
- 004_some-name_user_renamed_DMM.wpt
- 004_some-name_user_renamed_BBox.wpt
- Flightplan ready to import into GTN750: 004_some-name_fpl.gfp
