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
	"/eos/user/c/chenguan/Tuples/ForEleTrck/ParentFilesOfTheMINIAODSIM/59D09373-374D-B240-960C-49378B63160F.root",
	"/eos/user/c/chenguan/Tuples/ForEleTrck/ParentFilesOfTheMINIAODSIM/A9B78F21-6E3C-D048-8A84-CCE91B132E6B.root",
	"/eos/user/c/chenguan/Tuples/ForEleTrck/ParentFilesOfTheMINIAODSIM/BE588B52-D13C-2E45-BD64-BA936AD3BCEF.root",
	"/eos/user/c/chenguan/Tuples/ForEleTrck/ParentFilesOfTheMINIAODSIM/CF2D1CF2-BC1D-0144-B3E7-DBA2B2EAFE35.root",
	])

handle_electrons  = Handle ("std::vector<reco::GsfElectron>")
handle_vtx = Handle ("std::vector<reco::Vertex>")

label_electrons = ("gedGsfElectrons")
label_vtx = ("offlinePrimaryVertices")

# Create list,dict,pandas for print format
list = []

# Open ids as filter
with open('/afs/cern.ch/work/c/chenguan/FWLitePython/TrkStudies/electron_track/Bridge/ids.json','r') as fp:
	ids = json.load(fp)['id']
print len(ids)
# loop over events
for i,event in enumerate(events):
    #if i > options.maxEvents: break
    
    # for good vertex
    event.getByLabel (label_vtx, handle_vtx)
    vertices = handle_vtx.product()
    vtx_index = goodvertex(vertices)
    if vtx_index < 0 : continue
	    
    # extract all electrons
    event.getByLabel (label_electrons, handle_electrons)
    electrons = handle_electrons.product() 
    numEles = len (electrons)
    if numEles != 2: continue
    
    id = int(str(event.eventAuxiliary().run())+str(event.eventAuxiliary().luminosityBlock())+str(event.eventAuxiliary().event()))
    findid = False
    for tmp_id in ids:
	if tmp_id == id:
		findid = True
		break
    if findid == False: continue
    
    inner = [event.eventAuxiliary().run(),event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event(),]
    pos = []
    neg = []
    for electron in electrons:
	   v4 = ROOT.TLorentzVector()
	   v4.SetPtEtaPhiM(electron.pt(),electron.eta(),electron.phi(),electron.mass())
	   tmp = [
		electron.charge(),
		float("{:.5f}".format(electron.mass())),
		float("{:.3f}".format(electron.pt())),
		float("{:.3f}".format(electron.gsfTrack().pt())),
		float("{:.3f}".format(electron.eta())),
		float("{:.3f}".format(electron.gsfTrack().eta())),
		float("{:.3f}".format(electron.phi())),
		float("{:.3f}".format(electron.gsfTrack().phi())),
		float("{:.3f}".format(electron.correctedEcalEnergy())),
		float("{:.3f}".format(v4.Energy())),
		]
	   if electron.charge() > 0:
		   pos = tmp
	   else:
		   neg = tmp	
    inner = inner + pos + neg
    		   	
    list.append(inner)

cols = [
	'runNum',
	'LumiBlock',
	'eventNum',

	'pos_charge',
	'pos_electron_mass',
	'pos_electron_pt',
	'pos_gsfTrack_pt',
	'pos_electron_eta',
	'pos_gsfTrack_eta',
	'pos_electron_phi',
	'pos_gsfTrack_phi',
	'pos_correctedEcalEnergy',
	'pos_EnergyManually',

	'neg_charge',
	'neg_electron_mass',
	'neg_electron_pt',
	'neg_gsfTrack_pt',
	'neg_electron_eta',
	'neg_gsfTrack_eta',
	'neg_electron_phi',
	'neg_gsfTrack_phi',
	'neg_correctedEcalEnergy',
	'neg_EnergyManually',
]

# print columns template for html table
with open('../Bridge/aod_columns.txt','w') as tmp:
	for l in cols:
		tmp.write(l + '\n')
	tmp.close()

# print table and dump to json
df = pd.DataFrame(list, columns=cols)
result = df.to_json('../Bridge/aod_Zee.json',orient='index')
print df
