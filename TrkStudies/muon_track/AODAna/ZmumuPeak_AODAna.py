#! /usr/bin/env python3

from builtins import range
import ROOT
import sys
from DataFormats.FWLite import Events, Handle
import pandas as pd
import numpy as np

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
events = Events ("/eos/user/c/chenguan/Tuples/ForEleTrck/ParentFilesOfTheMINIAODSIM/13631887-2D4C-2F4A-8575-59FBD01348E7.root")
maxEvents = 100
# create handle outside of loop
handle  = Handle ("std::vector<reco::GsfElectron>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label = ("gedGsfElectrons")

# Create histograms, etc.
ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.gROOT.SetStyle('Plain') # white background
zmassHist = ROOT.TH1F ("zmass", "Z Candidate Mass", 50, 20, 220)

# Create list,dict,pandas for print format
list = []

# loop over events
for i,event in enumerate(events):
    if i > maxEvents: break
    print event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event()
    # use getByLabel, just like in cmsRun
    event.getByLabel (label, handle)
    # get the product
    eles = handle.product()
    # use eles to make Z peak
    numEles = len (eles)
    if numEles < 2: continue
    for outer in range (numEles - 1):
        outerEle = eles[outer]
        for inner in range (outer + 1, numEles):
            innerEle = eles[inner]
            if outerEle.charge() * innerEle.charge() >= 0:
                continue
            '''
	    inner4v = ROOT.TLorentzVector (innerMuon.px(), innerMuon.py(),
                                           innerMuon.pz(), innerMuon.energy())
            outer4v = ROOT.TLorentzVector (outerMuon.px(), outerMuon.py(),
                                           outerMuon.pz(), outerMuon.energy())
            zmassHist.Fill( (inner4v + outer4v).M() )
	    '''
	    ##test
	    list.append([innerEle.gsfTrack().px(), innerEle.trackMomentumAtVtx().X(), innerEle.trackMomentumAtCalo().X(), innerEle.trackMomentumOut().X(), innerEle.trackMomentumAtEleClus().X(), innerEle.trackMomentumAtVtxWithConstraint().X() ])
df = pd.DataFrame(list, columns=['px from gsfTrack','px at vtx','px at calo','px at seed','px at ele','px at vtx with constr'])
print df
# make a canvas, draw, and save it
c1 = ROOT.TCanvas()
zmassHist.Draw()
c1.Print ("zmass_py.png")
