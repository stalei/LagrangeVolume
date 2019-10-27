#  © Shahram Talei @ 2019 The University of Alabama - All rights reserved.
#you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
import yt
import numpy as np
from yt.analysis_modules.halo_finding.api import *
from yt.analysis_modules.halo_analysis.api import *





#how to run: python FindLV.py final_snapshot_file first_snapshot_file halo_catalog halo_id
#example: $python FindLV.py snap_264 snap_000 halos_0.0.ascii 12

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("snap", type=str)
    parser.add_argument("halo",type=str)
    parser.add_argument("contamination", type=int)
    parser.add_argument("extractshape", type=int)
    args = parser.parse_args()
    ds = yt.load(args.snap)#, unit_base=unit_base1)#,unit_system='galactic')
    if ds is None:
        print ("Error, sorry, I couldn't read the snapshot.!")
        sys.exit(1)
    print("Length unit: ", ds.length_unit.in_units('Mpc'))
    print("Time unit: ", ds.time_unit.in_units('Gyr'))
    print("Mass unit: ", ds.mass_unit.in_units('Msun'))
    print("Velocity unit: ", ds.velocity_unit.in_units('km/s'))
    #dh=yt.load(args.halo)
    dh=np.genfromtxt(args.halo, skip_header=18)
    if dh is None:
        print ("Error, sorry, I couldn't read the halo binary file.!")
        sys.exit(1)
    Idh=np.array(dh[:,0])
    #CountAll= len(id)
    p=5000
    UpperMass=1.0e13
    LowerMass=1.5e11
    pnumh=np.array(dh[:,1])
    Mvirh=np.array(dh[:,2])
    Rvirh=np.array(dh[:,4])# in kpc
    xhalo=np.array(dh[:,8])
    yhalo=np.array(dh[:,9])
    zhalo=np.array(dh[:,10])
