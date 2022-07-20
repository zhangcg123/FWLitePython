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

events = Events (["/eos/home-c/chenguan/Tuples/ForEleTrck/APieceOfDYMINIAODSIM/001C8DDF-599C-5E45-BF2C-76F887C9ADE9.root",
	"/eos/home-c/chenguan/Tuples/ForEleTrck/APieceOfDYMINIAODSIM/01522709-8919-C542-91B2-2262F3995F48.root",
	"/eos/home-c/chenguan/Tuples/ForEleTrck/APieceOfDYMINIAODSIM/015753DA-CD2E-F546-9A7B-9DD451DEA159.root",
	])

# create handle outside of loop
handle_electrons  = Handle ("std::vector<pat::Electron>")
handle_vtx = Handle ("std::vector<reco::Vertex>")

# for now, label is just a tuple of strings that is initialized just
label_electrons = ("slimmedElectrons")
label_vtx = ("offlineSlimmedPrimaryVertices")

# Create list,dict,pandas for print format
list = []
runNumbers = []

# Create histo
massZ_comb_ptetaphim = ROOT.TH1F('massz_comb','',300,70,110)
#massZ_comb_ptetaphim_forceelemass = ROOT.TH1F('massz_comb_ptetaphim_forceelemass','',300,70,110)
#massZ_comb_pxpypze = ROOT.TH1F('massz_comb_pxpypze','',300,70,110)

massZ_ecal_removecomb = ROOT.TH1F('massz_ecal_removecomb','',300,70,110)
#massZ_ecal_fromtrk = ROOT.TH1F('massz_ecal_fromtrk','',300,70,110)

#massZ_trkxyze = ROOT.TH1F('massz_trkxyze','',300,70,110)
#massZ_trkxyzm = ROOT.TH1F('massz_trkxyzm','',300,70,110)
#massZ_trkxyzm_forceelemass = ROOT.TH1F('massz_trkxyzm_forceelemass','',300,70,110)
massZ_trkptetaphim = ROOT.TH1F('massz_trkmode_ptetaphim','',300,70,110)
#massZ_trkptetaphim_forceelemass = ROOT.TH1F('massz_trkptetaphim_forceelemass','',300,70,110)

#massZ_trkmean_xyzm = ROOT.TH1F('massz_trkmean_xyzm','',300,70,110)
massZ_trkmean_xyze = ROOT.TH1F('massz_trkmean_xyze','',300,70,110)

#massZ_trkext_xyze = ROOT.TH1F('massz_vtxmomxyze','',300,70,110)
massZ_trkext_xyzm = ROOT.TH1F('massz_trkext_xyzm','',300,70,110)

massZ_trkbs_xyzm = ROOT.TH1F('massz_trkrbs_xyzm','',300,70,110)

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
    if len(electrons) != 2: continue
    tightelectrons = goodelectrons_miniaod( electrons )
    if len(tightelectrons) != 2: continue

    # z mass window
    pos = ROOT.TLorentzVector()
    neg = ROOT.TLorentzVector()
    pos.SetPtEtaPhiM(tightelectrons[0].pt(),tightelectrons[0].eta(),tightelectrons[0].phi(),tightelectrons[0].mass())
    neg.SetPtEtaPhiM(tightelectrons[1].pt(),tightelectrons[1].eta(),tightelectrons[1].phi(),tightelectrons[1].mass())
    massz_comb_ptetaphim = ( pos + neg ).M()	# ecal corrected, ecal trk combined, no s&s implemented
    if massz_comb_ptetaphim < 70 or massz_comb_ptetaphim > 110: continue
    massZ_comb_ptetaphim.Fill( massz_comb_ptetaphim )
    #print 'massz_comb_ptetaphim', '{:.3f}'.format(pos.P()), '{:.3f}'.format(pos.Energy()), '{:.3f}'.format(tightelectrons[0].userFloat('ecalTrkEnergyPreCorr'))

    ##########################
    #                        #
    ##########################
    #pos.SetPtEtaPhiM(tightelectrons[0].pt(),tightelectrons[0].eta(),tightelectrons[0].phi(),0.0005)
    #neg.SetPtEtaPhiM(tightelectrons[1].pt(),tightelectrons[1].eta(),tightelectrons[1].phi(),0.0005)
    #massz_comb_ptetaphim_forceelemass = ( pos + neg ).M()
    #massZ_comb_ptetaphim_forceelemass.Fill(massz_comb_ptetaphim_forceelemass)
    #print "{:.3f}".format(massz_comb_ptetaphim), "{:.3f}".format(massz_comb_ptetaphim_forceelemass), "{:.3f}".format(tightelectrons[0].mass()), '0.0005'
    #print 'massz_comb_ptetaphim_forceelemass', '{:.3f}'.format(pos.P()), '{:.3f}'.format(pos.Energy()), '{:.3f}'.format(tightelectrons[0].userFloat('ecalTrkEnergyPreCorr'))
    #
    #pos.SetPxPyPzE(tightelectrons[0].px(),tightelectrons[0].py(),tightelectrons[0].pz(),tightelectrons[0].userFloat('ecalTrkEnergyPreCorr'))
    #neg.SetPxPyPzE(tightelectrons[1].px(),tightelectrons[1].py(),tightelectrons[1].pz(),tightelectrons[1].userFloat('ecalTrkEnergyPreCorr'))
    #massz_comb_pxpypze = ( pos + neg ).M()
    #massZ_comb_pxpypze.Fill( massz_comb_pxpypze )
    #print "{:.3f}".format(massz_comb_pxpypze), "{:.3f}".format(massz_comb_ptetaphim), "{:.3f}".format(pos.M()), "{:.3f}".format(tightelectrons[0].mass())
    #print 'massz_comb_ptxyze', '{:.3f}'.format(pos.P()), '{:.3f}'.format(pos.Energy()), '{:.3f}'.format(tightelectrons[0].userFloat('ecalTrkEnergyPreCorr'))
    #				# just test three different ways to biuld electron, apart from, the electron mass, all them are the same exactlly.
    #				# I commented above two, the 1st one will be used for further studies.
    #				# electorn momenta magnitude = electron ecal energy, which is the core of the reconstruction of egamma.
    #				# because the momenta-energy relation E^2 = p^2 + m^2(c = 1). The impact from electron mass(too light) is negligibel
    #########################

    ##########################
    #                        #
    ##########################
    # z mass with ecal only
    ecalonly1 = ROOT.TLorentzVector()
    ecalonly2 = ROOT.TLorentzVector()
    corr1 = tightelectrons[0].correctedEcalEnergy()/tightelectrons[0].userFloat('ecalTrkEnergyPreCorr')
    corr2 = tightelectrons[1].correctedEcalEnergy()/tightelectrons[1].userFloat('ecalTrkEnergyPreCorr')
    ecalonly1.SetPxPyPzE(tightelectrons[0].px()*corr1,tightelectrons[0].py()*corr1,tightelectrons[0].pz()*corr1,tightelectrons[0].correctedEcalEnergy())
    ecalonly2.SetPxPyPzE(tightelectrons[1].px()*corr2,tightelectrons[1].py()*corr2,tightelectrons[1].pz()*corr2,tightelectrons[1].correctedEcalEnergy())
    massz_ecal_removecomb = ( ecalonly1 + ecalonly2 ).M()
    massZ_ecal_removecomb.Fill( massz_ecal_removecomb )
    # below should be the same or similar to above one?
    #corr1 = tightelectrons[0].correctedEcalEnergy()/tightelectrons[0].trackMomentumAtVtx().R()
    #corr2 = tightelectrons[1].correctedEcalEnergy()/tightelectrons[1].trackMomentumAtVtx().R()
    #ecalonly1.SetPxPyPzE(tightelectrons[0].trackMomentumAtVtx().X()*corr1,tightelectrons[0].trackMomentumAtVtx().Y()*corr1,tightelectrons[0].trackMomentumAtVtx().Z()*corr1,tightelectrons[0].correctedEcalEnergy())
    #ecalonly2.SetPxPyPzE(tightelectrons[1].trackMomentumAtVtx().X()*corr2,tightelectrons[1].trackMomentumAtVtx().Y()*corr2,tightelectrons[1].trackMomentumAtVtx().Z()*corr2,tightelectrons[1].correctedEcalEnergy())
    #massz_ecal_fromtrk = ( ecalonly1 + ecalonly2 ).M()
    #massZ_ecal_fromtrk.Fill( massz_ecal_fromtrk )
    #print '{:.3f}'.format(massz_ecal_fromtrk), '{:.3f}'.format(massz_ecal_removecomb)
    # 
    #
    #	#the check is trivial. of course they are the same, no matter what the trakc momenta is. Anyway, the combined and ecal only electorns are ready, let's move on to track only
    #
    #
    ########################

    # z mass with track only (gsfTrack.Mode)
    trk1 = ROOT.TLorentzVector()
    trk2 = ROOT.TLorentzVector()
    #trk1.SetPxPyPzE(tightelectrons[0].gsfTrack().pxMode(),tightelectrons[0].gsfTrack().pyMode(),tightelectrons[0].gsfTrack().pzMode(),tightelectrons[0].gsfTrack().pMode())
    #trk1.SetPxPyPzE(tightelectrons[1].gsfTrack().pxMode(),tightelectrons[1].gsfTrack().pyMode(),tightelectrons[1].gsfTrack().pzMode(),tightelectrons[1].gsfTrack().pMode())
    #massz_trkxyze = ( trk1 + trk2 ).M()
    #massZ_trkxyze.Fill( massz_trkxyze )
    
    trk1.SetPtEtaPhiM(tightelectrons[0].gsfTrack().ptMode(),tightelectrons[0].gsfTrack().etaMode(),tightelectrons[0].gsfTrack().phiMode(),tightelectrons[0].mass())
    trk2.SetPtEtaPhiM(tightelectrons[1].gsfTrack().ptMode(),tightelectrons[1].gsfTrack().etaMode(),tightelectrons[1].gsfTrack().phiMode(),tightelectrons[1].mass())
    massz_trkptetaphim = ( trk1 + trk2 ).M()
    massZ_trkptetaphim.Fill( massz_trkptetaphim )

    #trk1.SetXYZM(tightelectrons[0].gsfTrack().pxMode(),tightelectrons[0].gsfTrack().pyMode(),tightelectrons[0].gsfTrack().pzMode(),tightelectrons[0].mass())
    #trk2.SetXYZM(tightelectrons[1].gsfTrack().pxMode(),tightelectrons[1].gsfTrack().pyMode(),tightelectrons[1].gsfTrack().pzMode(),tightelectrons[1].mass())
    #massz_trkxyzm = ( trk1 + trk2 ).M()
    #massZ_trkxyzm.Fill( massz_trkxyzm )


    #trk1.SetPtEtaPhiM(tightelectrons[0].gsfTrack().ptMode(),tightelectrons[0].gsfTrack().etaMode(),tightelectrons[0].gsfTrack().phiMode(),0.00051)
    #trk2.SetPtEtaPhiM(tightelectrons[1].gsfTrack().ptMode(),tightelectrons[1].gsfTrack().etaMode(),tightelectrons[1].gsfTrack().phiMode(),0.00051)
    #massz_trkptetaphim_forceelemass = ( trk1 + trk2 ).M()
    #massZ_trkptetaphim_forceelemass.Fill( massz_trkptetaphim_forceelemass )

    #trk1.SetXYZM(tightelectrons[0].gsfTrack().pxMode(),tightelectrons[0].gsfTrack().pyMode(),tightelectrons[0].gsfTrack().pzMode(),0.00051)
    #trk2.SetXYZM(tightelectrons[1].gsfTrack().pxMode(),tightelectrons[1].gsfTrack().pyMode(),tightelectrons[1].gsfTrack().pzMode(),0.00051)
    #massz_trkxyzm_forceelemass = ( trk1 + trk2 ).M()
    #massZ_trkxyzm_forceelemass.Fill( massz_trkxyzm_forceelemass )
    #
    # the first one always give z mass = 0. why?
    # apart from the first one, all others give the same result. Right now, the second one used temporarily
    #
    ########################
    
    # z mass with trakc only (gsfTrack. Mean)
    trk1.SetPxPyPzE(tightelectrons[0].gsfTrack().px(),tightelectrons[0].gsfTrack().py(),tightelectrons[0].gsfTrack().pz(),tightelectrons[0].gsfTrack().p())
    trk2.SetPxPyPzE(tightelectrons[1].gsfTrack().px(),tightelectrons[1].gsfTrack().py(),tightelectrons[1].gsfTrack().pz(),tightelectrons[1].gsfTrack().p())
    massz_trkmean_xyze = ( trk1 + trk2 ).M()
    massZ_trkmean_xyze.Fill( massz_trkmean_xyze )
    
    #trk1.SetXYZM(tightelectrons[0].gsfTrack().px(),tightelectrons[0].gsfTrack().py(),tightelectrons[0].gsfTrack().pz(),tightelectrons[0].mass())
    #trk2.SetXYZM(tightelectrons[1].gsfTrack().px(),tightelectrons[1].gsfTrack().py(),tightelectrons[1].gsfTrack().pz(),tightelectrons[1].mass())
    #massz_trkmean_xyzm = (trk1+trk2).M()
    #massZ_trkmean_xyzm.Fill(massz_trkmean_xyzm)
    #
    #
    ########################
    

    # trakc moment from track extras
    trk1.SetXYZM(tightelectrons[0].trackMomentumAtVtx().X(),tightelectrons[0].trackMomentumAtVtx().Y(),tightelectrons[0].trackMomentumAtVtx().Z(),0.00051)
    trk2.SetXYZM(tightelectrons[1].trackMomentumAtVtx().X(),tightelectrons[1].trackMomentumAtVtx().Y(),tightelectrons[1].trackMomentumAtVtx().Z(),0.00051)
    massz_trkext_xyzm = ( trk1 + trk2 ).M()
    massZ_trkext_xyzm.Fill(massz_trkext_xyzm)

    #trk1.SetPxPyPzE(tightelectrons[0].trackMomentumAtVtx().X(),tightelectrons[0].trackMomentumAtVtx().Y(),tightelectrons[0].trackMomentumAtVtx().Z(),tightelectrons[0].trackMomentumAtVtx().R())
    #trk2.SetPxPyPzE(tightelectrons[1].trackMomentumAtVtx().X(),tightelectrons[1].trackMomentumAtVtx().Y(),tightelectrons[1].trackMomentumAtVtx().Z(),tightelectrons[1].trackMomentumAtVtx().R())
    #massz_trkext_xyze = ( trk1 + trk2 ).M()
    #massZ_trkext_xyze.Fill( massz_trkext_xyze )
    #
    # above two are the same
    #

    #
    # 
    trk1.SetXYZM(tightelectrons[0].trackMomentumAtVtxWithConstraint().X(),tightelectrons[0].trackMomentumAtVtxWithConstraint().Y(),tightelectrons[0].trackMomentumAtVtxWithConstraint().Z(),0.00051)
    trk2.SetXYZM(tightelectrons[1].trackMomentumAtVtxWithConstraint().X(),tightelectrons[1].trackMomentumAtVtxWithConstraint().Y(),tightelectrons[1].trackMomentumAtVtxWithConstraint().Z(),0.00051)
    massz_trkbs_xyzm = (trk1+trk2).M()
    massZ_trkbs_xyzm.Fill( massz_trkbs_xyzm )


    
    #tablesummary( event, tightelectrons, list, runNumbers )

'''
# print columns template for hmlt table
with open('../Bridge/miniaod_columns.txt','w') as tmp:
	for l in cols:
		tmp.write(l + '\n')
	tmp.close()

# print table and dump to json
df = pd.DataFrame(list, columns=cols)
print df
#result = df.to_json('../Bridge/miniaod_Zee.json',orient='index')

# print event index for aod analyzer
print len(runNumbers)
with open('../Bridge/ids.json','w') as json_file:
	json.dump({'id':runNumbers}, json_file)
'''



# root histogram
fout = ROOT.TFile('./roodataset.root','recreate')
massZ_comb_ptetaphim.Write()
massZ_ecal_removecomb.Write()
massZ_trkptetaphim.Write()
massZ_trkmean_xyze.Write()
massZ_trkext_xyzm.Write()
massZ_trkbs_xyzm.Write()
fout.Close()
