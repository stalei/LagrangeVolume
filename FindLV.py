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
import argparse




#how to run: python FindLV.py final_snapshot_file first_snapshot_file halo_catalog halo_id
#example: $python FindLV.py snap_263 ics_256_100.dat halos_0.0_G.bin 11

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
    dh =np.genfromtxt(args.HaloCatalog, skip_header=18)# yt.load('halos_0.0_G.bin')#args.HaloCatalog)
    if dh is None:
        print ("Error, sorry, I couldn't read the halo binary file.!")
        sys.exit(1)
    #adh = dh.all_data()
    # halo masses
    #dh.field_list()
    #print(ad["halos", "particle_mass"])
    #hMv=adh["halos", "particle_mass"]
    hRv=np.array(dh[:,4])#adh["halos", "virial_radius"]
    hid=np.array(dh[:,0])#adh["halos", "particle_identifier"] # particle_position_(x,y,z)
    hx=np.array(dh[:,8])#adh["halos", "particle_position_x"]
    hy=np.array(dh[:,9])#adh["halos", "particle_position_y"]
    hz=np.array(dh[:,10])#adh["halos", "particle_position_z"]
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
    rF=np.sqrt((halox-xf.v)**2.+(haloy-yf.v)**2.+(haloz-zf.v)**2.)#np.sqrt((halox.v-xf.v)**2.+(haloy.v-yf.v)**2.+(haloz.v-zf.v)**2.)
    idList=idsF[rF<Rvir]
    #
    maxID=np.max(idList)
    minID=np.min(idList)
    print(idList.v)
    adi = dsinitial.all_data()
    coordinatesI = adi[("Halo","Coordinates")]
    xi=coordinatesI[:,0]
    yi=coordinatesI[:,1]
    zi=coordinatesI[:,2]
    idsI = adi[("Halo","ParticleIDs")] #ParticleIDs or particle_index
    print(coordinatesI[idsI.v<1000])
    #LagCoords=coordinatesI[idsI==idList]
    #print(LagCoords)
    boundary=np.zeros((2,3))
    for i in range(0,3):
        boundary[0,i]=10000;
    for i in range(0,3):
        ps=coordinatesI[:,i]
        for pid in idList:
        #for i in range(0,3):
            pi=ps[idsI==pid]
            if pi>boundary[1,i]:
                boundary[1,i]=pi;
            if pi<boundary[0,i]:
                boundary[0,i]=pi
    #boundary=np.zeros((2,3))
    #for i in range(0,3):
    #    boundary[0,i]=np.min(LagCoords[:,i]) # (min max, x y z)
    #    boundary[1,i]=np.max(Lagcoords[:,i])
    print("Lagrange box is min/max (x,y,z):")
    print(boundary)
    #
