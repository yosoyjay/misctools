#!/usr/bin/bas

if [[ $# -ne 2 ]]; 
then
  echo "Usage: $0 run-dir run-name"
  exit 1
fi

runDir=$1
runName=$2
start=2010-01-01
end=2010-01-31

# Move to run dir
echo "Moving to $runDir"
cd $runDir

# Combine results
autocombine.py -j 16 -o combined -t 1 1 30

# Extract transect
extractTransect -r $runName -C -d combined -t 1 -s $start -e $end -v hvel,salt,trcr_1 -n oc_channel -t oc_length.bp

# Make plots
makeTransects -j 16 -o images/transect -M Spectral_r $runName/data/transect/oc_channel_hvel_0_$start\_$end.nc $runName/data/transect/oc_channel_salt_0_$start\_$end.nc $runName/data/transect/oc_channel_trcr_1_0_$start\_$end.nc

# Animation
makeAnimation images/transect $runName

# Move back
echo "Moving back to `readlink -f ..`"
cd ..
