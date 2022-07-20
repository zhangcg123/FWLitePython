import ROOT
import sys
import os
sys.path.append('/afs/cern.ch/work/c/chenguan/private/pycommontool/')
from FileSystemClass import *
from PlotClass import *

dirs = DirTree()
dirs.mkrootdir('test_dummy')
path = dirs.root

lx = ROOT.TLatex()
lx.SetNDC()
lx.SetTextSize(0.05)
lx.SetTextFont(42)
lx.SetTextAlign(23)

def onebyone( dataset_list_fit, dataset_list_vis, fit=False ):
	
	for i,d in enumerate( dataset_list_fit ):
		frame1 = x.frame()
		frame1.SetTitle('')
		ds_v[i].plotOn( frame1, ROOT.RooFit.MarkerColor(1) )
		if fit:
			dcb.fitTo( dataset_list_fit[i] )
			dcb.plotOn( frame1, ROOT.RooFit.LineColor(1) )
		c1 = ROOT.TCanvas('c1','',1400,1000) 
		c1.cd()
		frame1.Draw()
		if fit:
			lx.DrawLatex(0.25,0.9,'#color['+str(1)+']{#sigma_{'+d.GetName().replace('massz_','')+'}:' + "{:.3f}".format(sigma.getVal())+'}')
		c1.Print( path + '/' + d.GetName() + '.png' )


def compare( dataset_list_fit, dataset_list_vis, fit=False ):

	for i,d in enumerate( dataset_list_fit ):
		if i == 0: c = ROOT.TCanvas('c','',1400,1000)
		c.cd()
		frame = x.frame()
		frame.SetTitle('') 
		dataset_list_vis[i].plotOn( frame, ROOT.RooFit.MarkerColor(i+1) )
		if fit:
			dcb.fitTo( dataset_list_fit[i] )
			dcb.plotOn( frame, ROOT.RooFit.LineColor(i+1) )
		if i != 0 :
			frame.Draw('same')
		else:
			frame.Draw()
		if fit:
			lx.DrawLatex(0.25,0.9 - i*0.07,'#color['+str(i+1)+']{#sigma_{'+d.GetName().replace('massz_','')+'}:' + "{:.3f}".format(sigma.getVal())+'}')
	c.SaveAs( path + '/' + d.GetName() + '.png' )


#########################################
#					#
#					#
#					#
#########################################

x = ROOT.RooRealVar('x','',70,110)

fin = ROOT.TFile('roodataset.root','read')

keys = fin.GetListOfKeys()
ds = []
ds_v = []
for i, k in enumerate(keys):
    h = k.ReadObj()
    h.SetDirectory(0)
    h.SetName(k.GetName())
    d = ROOT.RooDataHist( h.GetName(), '', ROOT.RooArgList( x ), ROOT.RooFit.Import( h ) )
    d_v = ROOT.RooDataHist( h.GetName(), '', ROOT.RooArgList( x ), ROOT.RooFit.Import( h.Rebin(5) ) )
    ds.append( d )
    ds_v.append( d_v )

mean = ROOT.RooRealVar('mean','',91,85,93)
sigma = ROOT.RooRealVar('sigma','',1,0,10)
a1 = ROOT.RooRealVar('a1','',5,0,10)
a2 = ROOT.RooRealVar('a2','',5,0,10)
n1 = ROOT.RooRealVar('n1','',5,0,10)
n2 = ROOT.RooRealVar('n2','',5,0,10)
dcb = ROOT.RooDoubleCB('dcb','',x,mean,sigma,a1,n1,a2,n2)

onebyone( ds, ds_v, False )
