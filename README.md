# garmin_fpl
Automated Garmin GTN750-readable flight plan (.gfp) creation from waypoint file (user.wpt).

Usage
* create sub-directory `<subdir_name>` with one or multiple exported waypoint files named `*_user.wpt`. 

`python create_gfp_from_userwpt.py <subdir_name>`
...runs all three scripts:
1) `WPnameChanger.py` which renames the waypoints (column 1) according to the project name (6 alpha-numeric characters)
2) `DEC2DMM.py` which transforms the coordinates from decimal to degrees and decimal minutes.
3) `wpt_to_gfp.py` which finally takes the transformed user waypoints and creates a .gfp file with the correct syntax.

   
