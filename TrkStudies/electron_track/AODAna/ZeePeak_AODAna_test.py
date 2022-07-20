#! /usr/bin/env python3

from builtins import range
import ROOT
import sys
from DataFormats.FWLite import Events, Handle
import pandas as pd
import numpy as np
import json
sys.path.append('/afs/cern.ch/work/c/chenguan/FWLitePython/TrkStudies/python/')
from helper import *
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing ('python')
options.parseArguments()

events = Events (["/eos/user/c/chenguan/Tuples/ForEleTrck/ParentFilesOfTheMINIAODSIM/13631887-2D4C-2F4A-8575-59FBD01348E7.root",
	#"/eos/user/c/chenguan/Tuples/ForEleTrck/ParentFilesOfTheMINIAODSIM/59D09373-374D-B240-960C-49378B63160F.root",
	#"/eos/user/c/chenguan/Tuples/ForEleTrck/ParentFilesOfTheMINIAODSIM/A9B78F21-6E3C-D048-8A84-CCE91B132E6B.root",
	#"/eos/user/c/chenguan/Tuples/ForEleTrck/ParentFilesOfTheMINIAODSIM/BE588B52-D13C-2E45-BD64-BA936AD3BCEF.root",
	#"/eos/user/c/chenguan/Tuples/ForEleTrck/ParentFilesOfTheMINIAODSIM/CF2D1CF2-BC1D-0144-B3E7-DBA2B2EAFE35.root",
	])

handle_electrons  = Handle ("std::vector<reco::GsfElectron>")
handle_vtx = Handle ("std::vector<reco::Vertex>")

label_electrons = ("gedGsfElectrons")
label_vtx = ("offlinePrimaryVertices")

# Create list,dict,pandas for print format
list = []

# loop over events
for i,event in enumerate(events):
    if i > options.maxEvents: break
	    
    # extract all electrons
    event.getByLabel (label_electrons, handle_electrons)
    electrons = handle_electrons.product() 
    
    inner = [event.eventAuxiliary().run(),event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event(),]
    for electron in electrons:
	   print electron.classification
	   v4 = ROOT.TLorentzVector()
	   v4.SetPxPyPzE(electron.trackMomentumAtVtxWithConstraint().X(),electron.trackMomentumAtVtxWithConstraint().Y(),electron.trackMomentumAtVtxWithConstraint().Z(),electron.correctedEcalEnergy())
	   tmp = [
		#electron.charge(),
		#float("{:.5f}".format(electron.mass())),
		float("{:.3f}".format(v4.Pt())),
		float("{:.3f}".format(electron.pt())),
		float("{:.3f}".format(electron.gsfTrack().pt())),
		float("{:.3f}".format(v4.Eta())),
		float("{:.3f}".format(electron.eta())),
		float("{:.3f}".format(electron.gsfTrack().eta())),
		float("{:.3f}".format(v4.Phi())),
		float("{:.3f}".format(electron.phi())),
		float("{:.3f}".format(electron.gsfTrack().phi())),
		
		float("{:.3f}".format(electron.correctedEcalEnergy())),
		float("{:.3f}".format(v4.Energy())),
		]
	   list.append( inner + tmp )
    		   	

cols = [
	'runNum',
	'LumiBlock',
	'eventNum',

	#'charge',
	#'electron_mass',
	'electron_bs_pt',
	'electron_pt',
	'gsfTrack_pt',
	'electron_bs_eta',
	'electron_eta',
	'gsfTrack_eta',
	'electron_bs_phi',
	'electron_phi',
	'gsfTrack_phi',
	'correctedEcalEnergy',
	'EnergyManually',
]

# print table and dump to json
df = pd.DataFrame(list, columns=cols)
print df[['electron_bs_pt','electron_pt','gsfTrack_pt','electron_bs_eta','electron_eta','gsfTrack_eta','electron_bs_phi','electron_phi','gsfTrack_phi']]
