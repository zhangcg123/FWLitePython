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
events = Events ("/eos/home-c/chenguan/Tuples/ForEleTrck/APieceOfDYMINIAODSIM/001C8DDF-599C-5E45-BF2C-76F887C9ADE9.root")
maxEvents = 100000

# create handle outside of loop
handle_muons  = Handle ("std::vector<pat::Muon>")
handle_vtx = Handle ("std::vector<reco::Vertex>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label_muons = ("slimmedMuons")
label_vtx = ("offlineSlimmedPrimaryVertices")

# Create histograms, etc.
ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.gROOT.SetStyle('Plain') # white background
zmassHist = ROOT.TH1F ("zmass", "Z Candidate Mass", 50, 20, 220)

# Create list,dict,pandas for print format
list = []

# loop over events
for i,event in enumerate(events):
    #if i > maxEvents: break
    
    # find good vertex
    event.getByLabel (label_vtx, handle_vtx)
    vertices = handle_vtx.product()
    vtx_index = goodvertex(vertices)
    if vtx_index < 0 : continue
    
    # two tight muons
    event.getByLabel (label_muons, handle_muons)
    muons = handle_muons.product()
    tightmuons = goodmuons_miniaod(muons, vertices[vtx_index])
    
    # re-store to json
    for muon in tightmuons:
	    ##test
	    list.append([event.eventAuxiliary().run(),event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event(),
	    	muon.charge(),muon.pt(),muon.eta(),muon.phi(),muon.mass()])
    
df = pd.DataFrame(list, columns=['runNum','LumiBlock','eventNum', 
	'muon_charge','muon_pt','muon_eta','muon_phi','muon_m',])
result = df.to_json('./miniaod_mumu.json',orient='index')
print df
'''

# make a canvas, draw, and save it
c1 = ROOT.TCanvas()
zmassHist.Draw()
c1.Print ("zmass_py.png")
'''
