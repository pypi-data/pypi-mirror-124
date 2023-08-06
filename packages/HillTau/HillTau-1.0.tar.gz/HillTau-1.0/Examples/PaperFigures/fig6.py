# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth
# Floor, Boston, MA 02110-1301, USA.
# 

'''
*******************************************************************
 * File:            fig6.py
 * Description:     Runs a series of models in MOOSE and HillTau to 
 *                  compare their runtimes.
 * Author:          Upinder S. Bhalla
 * E-mail:          bhalla@ncbs.res.in
 ********************************************************************/
'''
from __future__ import print_function
import sys
import os
import json
import re
import argparse
import numpy as np
import matplotlib.pyplot as plt
import time
import moose
import hillTau

t1 = 20
t2 = 60
t3 = 100
i1 = 1e-3

plotDt = 1

def runSim( chem, ht, runtime ):
    modelId = moose.loadModel( "KKIT_MODELS/" + chem, 'model', 'gsl' )
    for i in range( 10, 20 ):
        moose.setClock( i, plotDt )

    moose.reinit()
    mooseTime = time.time()
    moose.start( runtime )
    mooseTime = time.time() - mooseTime
    moose.delete( '/model' )

    jsonDict = hillTau.loadHillTau( "HT_MODELS/" + ht )
    hillTau.scaleDict( jsonDict, hillTau.getQuantityScale( jsonDict ) )
    model = hillTau.parseModel( jsonDict )
    model.dt = plotDt
    model.reinit()
    htTime = time.time()
    model.advance( runtime )
    htTime = time.time() - htTime

    # Now run it again, but in steady-state model for HillTau
    model.reinit()
    htTime2 = time.time()
    model.advance( runtime, settle = True )
    htTime2 = time.time() - htTime2
    print( "{:12s}  {:8.3f}  {:8.3f}  {:8.5f}   {:8.1f}".format( ht, mooseTime, htTime, htTime2, runtime ))
    #return [mooseTime, htTime, htTime2 ]

def main():
    kkitList = ["exc.g", "conv.g", "fb_inhib.g", "kholodenko.g", "bcm.g", "acc92_fixed.g", "autsim_v1_17Jul2020.g" ]
    htList = ["exc.json", "conv.json", "fb_inhib.json", "osc.json", "bcm.json", "syn_prot2.json", "aut6.json" ]
    runtime = [ 1e6, 1e6, 1e6, 1e6, 1e5, 1e4, 1e3]
    results = []
    print("Model            MOOSE       HT_time    HT_steady_state  simtime" )
    for k, h, t in zip( kkitList, htList, runtime ):
        runSim( k, h, t )
        #results.append( runSim( k, j, t ) )

if __name__ == '__main__':
    main()







