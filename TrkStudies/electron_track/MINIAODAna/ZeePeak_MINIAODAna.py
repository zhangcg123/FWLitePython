#! /usr/bin/env python3

from builtins import range
import ROOT
import sys
from DataFormats.FWLite import Events, Handle
import json
import pandas as pd
import numpy as np
sys.path.append('/afs/cern.ch/work/c/chenguan/FWLitePython/TrkStudies/python/')
from helper import *
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing ('python')
options.parseArguments()

events = Events ("/eos/home-c/chenguan/Tuples/ForEleTrck/APieceOfDYMINIAODSIM/001C8DDF-599C-5E45-BF2C-76F887C9ADE9.root")

# create handle outside of loop
handle_electrons  = Handle ("std::vector<pat::Electron>")
handle_vtx = Handle ("std::vector<reco::Vertex>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label_electrons = ("slimmedElectrons")
label_vtx = ("offlineSlimmedPrimaryVertices")

# Create list,dict,pandas for print format
list = []
runNumbers = []

# loop over events
for i,event in enumerate(events):
    #if i > options.maxEvents: break
    
    # find good vertex
    event.getByLabel (label_vtx, handle_vtx)
    vertices = handle_vtx.product()
    vtx_index = goodvertex(vertices)
    if vtx_index < 0 : continue
    
    # two tight electrons
    event.getByLabel (label_electrons, handle_electrons)
    electrons = handle_electrons.product()
    tightelectrons = goodelectrons_miniaod( electrons )
    if len(tightelectrons) !=2: continue

    # z mass window
    pos = ROOT.TLorentzVector()
    neg = ROOT.TLorentzVector()
    pos.SetPtEtaPhiM(tightelectrons[0].pt(),tightelectrons[0].eta(),tightelectrons[0].phi(),tightelectrons[0].mass())
    neg.SetPtEtaPhiM(tightelectrons[1].pt(),tightelectrons[1].eta(),tightelectrons[1].phi(),tightelectrons[1].mass())
    massz = ( pos + neg ).M()
    if massz < 70 or massz > 110: continue
    
    runNumbers.append(int(str(event.eventAuxiliary().run())+str(event.eventAuxiliary().luminosityBlock())+str(event.eventAuxiliary().event())))
     
    list.append([
    	event.eventAuxiliary().run(),
	event.eventAuxiliary().luminosityBlock(),
	event.eventAuxiliary().event(),
	
	tightelectrons[0].charge(),
	float("{:.5f}".format(tightelectrons[0].mass())),
	float("{:.3f}".format(tightelectrons[0].pt())),
	float("{:.3f}".format(tightelectrons[0].gsfTrack().pt())),
	float("{:.3f}".format(tightelectrons[0].eta())),
	float("{:.3f}".format(tightelectrons[0].gsfTrack().eta())),
	float("{:.3f}".format(tightelectrons[0].phi())),
	float("{:.3f}".format(tightelectrons[0].gsfTrack().phi())),
	float("{:.3f}".format(tightelectrons[0].correctedEcalEnergy())),
	float("{:.3f}".format(tightelectrons[0].userFloat('ecalEnergyPreCorr'))),
	float("{:.3f}".format(tightelectrons[0].userFloat('ecalTrkEnergyPreCorr'))),
	float("{:.3f}".format(pos.Energy())),
	float("{:.3f}".format(tightelectrons[0].userFloat('ecalEnergyPostCorr'))),
	float("{:.3f}".format(tightelectrons[0].userFloat('ecalTrkEnergyPostCorr'))),
	
	tightelectrons[1].charge(),
	float("{:.5f}".format(tightelectrons[1].mass())),
	float("{:.3f}".format(tightelectrons[1].pt())),
	float("{:.3f}".format(tightelectrons[1].gsfTrack().pt())),
	float("{:.3f}".format(tightelectrons[1].eta())),
	float("{:.3f}".format(tightelectrons[1].gsfTrack().eta())),
	float("{:.3f}".format(tightelectrons[1].phi())),
	float("{:.3f}".format(tightelectrons[1].gsfTrack().phi())),
	float("{:.3f}".format(tightelectrons[1].correctedEcalEnergy())),
	float("{:.3f}".format(tightelectrons[1].userFloat('ecalEnergyPreCorr'))),
	float("{:.3f}".format(tightelectrons[1].userFloat('ecalTrkEnergyPreCorr'))),
	float("{:.3f}".format(neg.Energy())),
	float("{:.3f}".format(tightelectrons[1].userFloat('ecalEnergyPostCorr'))),
	float("{:.3f}".format(tightelectrons[1].userFloat('ecalTrkEnergyPostCorr'))),

	float("{:.3f}".format(massz)),
	])

	


    cols = [ 
	'runNum',
	'LumiBlock',
	'eventNum', 
	
	'pos_charge',
	'pos_mass',
	'pos_pt',
	'pos_gsfTrack_pt',
	'pos_electron_eta',
	'pos_gsfTrack_eta',
	'pos_electron_phi',
	'pos_gsfTrack_phi',
	'pos_correctedEcalEnergy',
	'pos_ecalEnergyPreCorr',
	'pos_ecalTrkPreCorr',
	'pos_EnergyManually',
	'pos_ecalEnergyPostCorr',
	'pos_ecalTrkPostCorr',

	'neg_charge',
	'neg_mass',
	'neg_pt',
	'neg_gsfTrack_pt',
	'neg_electron_eta',
	'neg_gsfTrack_eta',
	'neg_electron_phi',
	'neg_gsfTrack_phi',
	'neg_correctedEcalEnergy',
	'neg_ecalEnergyPreCorr',
	'neg_ecalTrkPreCorr',
	'neg_EnergyManually',
	'neg_ecalEnergyPostCorr',
	'neg_ecalTrkPostCorr',

	'massz'
	]

# print columns template for hmlt table
with open('./columns.txt','w') as tmp:
	for l in cols:
		tmp.write(l + '\n')
	tmp.close()

# print table and dump to json
df = pd.DataFrame(list, columns=cols)
result = df.to_json('./miniaod_Zee.json',orient='index')
print df

# print event index for aod analyzer
print len(runNumbers)
with open('ids.json','w') as json_file:
	json.dump({'id':runNumbers}, json_file)
'''

# make a canvas, draw, and save it
c1 = ROOT.TCanvas()
zmassHist.Draw()
c1.Print ("zmass_py.png")
'''
