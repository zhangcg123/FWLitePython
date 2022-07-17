import ROOT
import sys
import os
import json
import pandas as pd
sys.path.append('/afs/cern.ch/work/c/chenguan/private/pycommontool/')
from FileSystemClass import *
from HTMLClass import *

dirs = DirTree()
dirs.mkrootdir('test_'+os.getcwd().split('/')[-1])
path = dirs.root

myhtml = HTMLClass('Z to ee info for electron track study')
myhtml.section('section1, test...')
string = myhtml.check()

df = pd.read_json('aod_Zee.json',orient='index')
cols = df.columns.tolist()

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
   'electron_energyMaunually',
]
df = df[cols]

string = string + '\n' + df.to_html()
fp = open(path + '/test.html','w')
fp.write(string)
fp.close()
