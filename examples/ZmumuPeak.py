#! /usr/bin/env python3

from builtins import range
import ROOT
import sys
from DataFormats.FWLite import Events, Handle

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
events = Events ("root://cms-xrd-global.cern.ch///store/mc/RunIISummer20UL18MiniAODv2/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/120000/001C8DDF-599C-5E45-BF2C-76F887C9ADE9.root")
#maxEvents = 100
# create handle outside of loop
handle  = Handle ("std::vector<pat::Muon>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label = ("slimmedMuons")

# Create histograms, etc.
ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.gROOT.SetStyle('Plain') # white background
zmassHist = ROOT.TH1F ("zmass", "Z Candidate Mass", 50, 20, 220)

# loop over events
for i,event in enumerate(events):
    #if i > options.maxEvents: break
    # use getByLabel, just like in cmsRun
    event.getByLabel (label, handle)
    # get the product
    muons = handle.product()
    # use muons to make Z peak
    numMuons = len (muons)
    if numMuons < 2: continue
    for outer in range (numMuons - 1):
        outerMuon = muons[outer]
        for inner in range (outer + 1, numMuons):
            innerMuon = muons[inner]
            if outerMuon.charge() * innerMuon.charge() >= 0:
                continue
            '''
	    inner4v = ROOT.TLorentzVector (innerMuon.px(), innerMuon.py(),
                                           innerMuon.pz(), innerMuon.energy())
            outer4v = ROOT.TLorentzVector (outerMuon.px(), outerMuon.py(),
                                           outerMuon.pz(), outerMuon.energy())
            zmassHist.Fill( (inner4v + outer4v).M() )
	    '''
	    ##test
	    print i,innerMuon.muonBestTrack().pt(), innerMuon.pt(),innerMuon.muonBestTrack().eta(),innerMuon.eta()

# make a canvas, draw, and save it
c1 = ROOT.TCanvas()
zmassHist.Draw()
c1.Print ("zmass_py.png")
