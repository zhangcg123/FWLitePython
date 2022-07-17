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
