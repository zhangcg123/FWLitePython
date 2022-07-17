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

# Make VarParsing object
# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#VarParsing_Example
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')
options.parseArguments()

# Events takes either
# - single file name
# - list of file names
# - VarParsing options

# use Varparsing object
#events = Events (options)
# use single file name
events = Events (["/eos/user/c/chenguan/Tuples/ForEleTrck/ParentFilesOfTheMINIAODSIM/13631887-2D4C-2F4A-8575-59FBD01348E7.root",
	"/eos/user/c/chenguan/Tuples/ForEleTrck/ParentFilesOfTheMINIAODSIM/59D09373-374D-B240-960C-49378B63160F.root",
	"/eos/user/c/chenguan/Tuples/ForEleTrck/ParentFilesOfTheMINIAODSIM/A9B78F21-6E3C-D048-8A84-CCE91B132E6B.root",
	"/eos/user/c/chenguan/Tuples/ForEleTrck/ParentFilesOfTheMINIAODSIM/BE588B52-D13C-2E45-BD64-BA936AD3BCEF.root",
	"/eos/user/c/chenguan/Tuples/ForEleTrck/ParentFilesOfTheMINIAODSIM/CF2D1CF2-BC1D-0144-B3E7-DBA2B2EAFE35.root",
	])
maxEvents = 100
# create handle outside of loop
handle_electrons  = Handle ("std::vector<reco::GsfElectron>")
handle_vtx = Handle ("std::vector<reco::Vertex>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label_electrons = ("gedGsfElectrons")
label_vtx = ("offlinePrimaryVertices")

# Create histograms, etc.
#ROOT.gROOT.SetBatch()        # don't pop up canvases
#ROOT.gROOT.SetStyle('Plain') # white background
#zmassHist = ROOT.TH1F ("zmass", "Z Candidate Mass", 50, 20, 220)

# Create list,dict,pandas for print format
list = []

# Open ids as filter
with open('/afs/cern.ch/work/c/chenguan/FWLitePython/TrkStudies/electron_track/MINIAODAna/ids.json','r') as fp:
	ids = json.load(fp)['id']
print ids
# loop over events
for i,event in enumerate(events):
    #if i > maxEvents: break
    
    # for good vertex
    event.getByLabel (label_vtx, handle_vtx)
    vertices = handle_vtx.product()
    vtx_index = goodvertex(vertices)
    if vtx_index < 0 : continue
	    
    # extract all electrons
    event.getByLabel (label_electrons, handle_electrons)
    electrons = handle_electrons.product() 
    numEles = len (electrons)
    if numEles < 2: continue
    
    id = int(str(event.eventAuxiliary().run())+str(event.eventAuxiliary().luminosityBlock())+str(event.eventAuxiliary().event()))
    findid = False
    for tmp_id in ids:
	if tmp_id == id:
		findid = True
		break
    if findid == False: continue
    
    for electron in electrons:
	   v4 = ROOT.TLorentzVector()
	   v4.SetPtEtaPhiM(electron.pt(),electron.eta(),electron.phi(),electron.mass())
	   list.append([
	   	event.eventAuxiliary().run(),
		event.eventAuxiliary().luminosityBlock(),
		event.eventAuxiliary().event(),
		electron.charge(),
		electron.mass(),
		electron.pt(),
		electron.gsfTrack().pt(),
		electron.eta(),
		electron.gsfTrack().eta(),
		electron.phi(),
		electron.gsfTrack().phi(),
		electron.correctedEcalEnergy(),
		v4.Energy(),
		])
    cols = [
    	'runNum',
	'LumiBlock',
	'eventNum',
	'electron_charge',
	'electron_mass',
	'electron_pt',
	'gsfTrack_pt',
	'electron_eta',
	'gsfTrack_eta',
	'electron_phi',
	'gsfTrack_phi',
	'electron_correctedEcalEnergy',
	'electron_energyManually',
	]

df = pd.DataFrame(list, columns=cols)
result = df.to_json('./aod_Zee.json',orient='index')
print df
