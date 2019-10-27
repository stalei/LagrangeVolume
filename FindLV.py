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
    parser.add_argument("fsnap", type=str)
    parser.add_argument("isnap", type=str)
    parser.add_argument("HaloCatalog",type=str)
    parser.add_argument("TargetHalo", type=int)
    args = parser.parse_args()
    dsfinal = yt.load(args.fsnap)#, unit_base=unit_base1)#,unit_system='galactic')
    dsinitial = yt.load(args.isnap)
    if dsfinal is None or dsinitial is None:
        print ("Error, sorry, I couldn't read the snapshot.!")
        sys.exit(1)
    #print("Length unit: ", ds.length_unit.in_units('Mpc'))
    #print("Time unit: ", ds.time_unit.in_units('Gyr'))
    #print("Mass unit: ", ds.mass_unit.in_units('Msun'))
    #print("Velocity unit: ", ds.velocity_unit.in_units('km/s'))
    #dh=yt.load(args.halo)
    dh = yt.load(args.HaloCatalog)
    if dh is None:
        print ("Error, sorry, I couldn't read the halo binary file.!")
        sys.exit(1)
    adh = dh.all_data()
    # halo masses
    #print(ad["halos", "particle_mass"])
    hMv=adh["halos", "particle_mass"]
    hRv=adh["halos", "virial_radius"]
    hid=adh["halos", "particle_identifier"]  particle_position_(x,y,z)
    hx=adh["halos", "particle_position_x"]
    hy=adh["halos", "particle_position_y"]
    hz=adh["halos", "particle_position_z"]
    #
    Rvir=hRv[hid==args.TargetHalo]
    Rvir/=1000. # convert to Mpc
    halox=hx[hid==args.TargetHalo]
    haloy=hy[hid==args.TargetHalo]
    haloz=hz[hid==args.TargetHalo]
    #
    adf = dsfinal.all_data()
    coordinatesF = adf[("Halo","Coordinates")]
    xf=coordinatesF[:,0]
    yf=coordinatesF[:,1]
    zf=coordinatesF[:,2]
    idsF = adf[("Halo","ParticleIDs")] #ParticleIDs or particle_index
    rF=np.sqrt((halox.v-xf.v)**2.+(haloy.v-yf.v)**2.+(haloz.v-zf.v)**2.)
    idList=idsF[rF<Rvir]
    #
    adi = dsfinal.all_data()
    coordinatesI = adi[("Halo","Coordinates")]
    idsI = adi[("Halo","ParticleIDs")] #ParticleIDs or particle_index
    LagCoords=coordinatesI[idsI==idList]
    boundary=np.zeros((2,3))
    for i in range(0,3):
        boundary[0,i]=np.min(LagCoords[:,i]) # (min max, x y z)
        boundary[1,i]=np.max(Lagcoords[:,i])
    print("Lagrange box is(x,y,z):")
    print(boundary)
    #
