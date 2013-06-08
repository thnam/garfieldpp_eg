#!/bin/sh
OSTYPE=$(uname)
if [ "$OSTYPE" == "Darwin" ]; then
	. ~/setenv.sh
	alias gmsh='/Applications/Gmsh.app/Contents/MacOS/gmsh'
	PATH=$PATH:/Applications/Elmer/bin/
	DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:/Applications/Elmer/lib
fi

target_name=cap
# Generate geometry description
./$target_name.py
# Mesh
gmsh $target_name.geo -3 -order 2
# Convert mesh files to Elmer format
ElmerGrid 14 2 $target_name.msh -autoclean
# Solve
ElmerSolver $target_name.sif
# Display
make
./test
