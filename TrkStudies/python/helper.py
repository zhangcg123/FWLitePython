import ROOT

def goodvertex( vertices ):
	theindex = -1;
	for i,vtx in enumerate( vertices ):
		if vtx.ndof() < 4 or vtx.position().Rho() > 2.0 or abs(vtx.position().Z()) > 24.0 or vtx.isFake(): continue
		else:
			theindex = i
			break
	return theindex

def goodelectrons_miniaod( electrons ):
	
	tightelectrons_list = []
	for ele in electrons:
		if ele.isElectronIDAvailable('cutBasedElectronID-Fall17-94X-V2-tight') and ele.electronID('cutBasedElectronID-Fall17-94X-V2-tight'):
			tightelectrons_list.append(ele)
	
	if len(tightelectrons_list) != 2:
		return []
	if tightelectrons_list[0].charge() * tightelectrons_list[1].charge() > 0:
		return []

	positron = tightelectrons_list[0]
	electron = tightelectrons_list[1]
	if tightelectrons_list[0].charge() < 0:
		positron = tightelectrons_list[1]
		electron = tightelectrons_list[0]
	return [positron,electron]

def goodmuons_miniaod( muons, vtx ):
	
	tightmuon_list = []
	for mu in muons:
		if mu.isTightMuon( vtx ):
			tightmuon_list.append(mu)
	
	if len(tightmuon_list) != 2: 
		return []
	elif tightmuon_list[0].charge() * tightmuon_list[1].charge() > 0:
		return []
	else:
		return tightmuon_list	
		
def tablesummary( evt, tighteles, list, runNumbers ):
    
    runNumbers.append(int(str(evt.eventAuxiliary().run())+str(evt.eventAuxiliary().luminosityBlock())+str(evt.eventAuxiliary().event())))
       
    list.append([
        evt.eventAuxiliary().run(),
        evt.eventAuxiliary().luminosityBlock(),
        evt.eventAuxiliary().event(),
        
        tighteles[0].charge(),
        float("{:.5f}".format(tighteles[0].mass())),
        float("{:.3f}".format(tighteles[0].pt())),
        float("{:.3f}".format(tighteles[0].gsfTrack().pt())),
        float("{:.3f}".format(tighteles[0].eta())),
        float("{:.3f}".format(tighteles[0].gsfTrack().eta())),
        float("{:.3f}".format(tighteles[0].phi())),
        float("{:.3f}".format(tighteles[0].gsfTrack().phi())),
        float("{:.3f}".format(tighteles[0].correctedEcalEnergy())),
        float("{:.3f}".format(tighteles[0].userFloat('ecalEnergyPreCorr'))),
        float("{:.3f}".format(tighteles[0].userFloat('ecalTrkEnergyPreCorr'))),
        float("{:.3f}".format(tighteles[0].userFloat('ecalEnergyPostCorr'))),
        float("{:.3f}".format(tighteles[0].userFloat('ecalTrkEnergyPostCorr'))),
        
        tighteles[1].charge(),
        float("{:.5f}".format(tighteles[1].mass())),
        float("{:.3f}".format(tighteles[1].pt())),
        float("{:.3f}".format(tighteles[1].gsfTrack().pt())),
        float("{:.3f}".format(tighteles[1].eta())),
        float("{:.3f}".format(tighteles[1].gsfTrack().eta())),
        float("{:.3f}".format(tighteles[1].phi())),
        float("{:.3f}".format(tighteles[1].gsfTrack().phi())),
        float("{:.3f}".format(tighteles[1].correctedEcalEnergy())),
        float("{:.3f}".format(tighteles[1].userFloat('ecalEnergyPreCorr'))),
        float("{:.3f}".format(tighteles[1].userFloat('ecalTrkEnergyPreCorr'))),
        float("{:.3f}".format(tighteles[1].userFloat('ecalEnergyPostCorr'))),
        float("{:.3f}".format(tighteles[1].userFloat('ecalTrkEnergyPostCorr'))),
       
        ])

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
        'pos_ecalEnergyPreCorr',
        'pos_ecalTrkPreCorr',
        'pos_ecalEnergyPostCorr',
        'pos_ecalTrkPostCorr',
           
        'neg_charge',
        'neg_electron_mass',
        'neg_electron_pt',
        'neg_gsfTrack_pt',
        'neg_electron_eta',
        'neg_gsfTrack_eta',
        'neg_electron_phi',
        'neg_gsfTrack_phi',
        'neg_correctedEcalEnergy',
        'neg_ecalEnergyPreCorr',
        'neg_ecalTrkPreCorr',
        'neg_ecalEnergyPostCorr',
        'neg_ecalTrkPostCorr',
]	
